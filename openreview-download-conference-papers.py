os.environ['OPENREVIEW_USERNAME'] = None # YOUR USERNAME from https://openreview.net/
os.environ['OPENREVIEW_PASSWORD'] = None # YOUR PASSWORD

import os
from collections import defaultdict
import openreview # pip install openreview-py
from tqdm import tqdm

def get_venues(client, confs, years):
  def filter_year(venue):
    for year in years:
      if year in venue:
        return venue
    return None
  venues = client.get_group(id='venues').members
  venues = list(map(filter_year, venues))
  venues = filter(lambda venue:venue is not None, venues)
  reqd_venues = []
  for venue in venues:
    for conf in confs:
      if conf.lower() in venue.lower():
        reqd_venues.append(venue)
        break
  reqd_venues = map(filter_year, reqd_venues)
  reqd_venues = list(filter(lambda venue:venue is not None, reqd_venues))
  return reqd_venues


def group_venues(venues, bins):
  def get_bins_dict():
    bins_dict = {bin:[] for bin in bins}
    return bins_dict
  
  bins_dict = get_bins_dict()
  for venue in venues:
    for bin in bins:
      if bin.lower() in venue.lower():
        bins_dict[bin].append(venue)
        break
  
  return bins_dict

def download_PDFs(metadata, output_dir=None):
    """
    Download PDFs for papers from OpenReview conferences.

    Args:
        metadata (dict): Dictionary containing submissions and reviews for each venue
        output_dir (str, optional): Directory to save PDFs. Defaults to None.
    """
    import requests
    import time

    # venue_id (str): Venue ID (e.g. "NeurIPS.cc/2024/Conference", or "ICLR.cc/2024/Conference")
    venue_id = list(metadata.keys())[0]

    def download_with_retry(url, max_retries=5):
        for attempt in range(max_retries):
            response = requests.get(url)
            if response.status_code == 200:
                return response
            elif response.status_code == 429:  # Too Many Requests
                wait_time = min(2 ** attempt, 32)  # Exponential backoff capped at 32 seconds
                time.sleep(wait_time)
                continue
            else:
                return response
        return response  # Return last response if all retries failed

    # Create directory if it doesn't exist
    if output_dir is None:
        output_dir = f'{venue_id}-pdfs'
    os.makedirs(output_dir, exist_ok=True)
    num_skips = 0
    num_fails = 0

    # Iterate through submissions and save content as JSON
    for submission in tqdm(metadata[venue_id]['submissions'], desc=f"Downloading PDFs for {venue_id}"):
        content = submission.content
        # Don't save rejected
        if 'Rejected_Submission' in content['venueid']['value'] or 'Withdrawn_Submission' in content['venueid']['value']:
            # print("skipping submission", content["title"]["value"])
            num_skips += 1
            continue
        
        title = content["title"]["value"].replace('/', '-').replace('\\', '-').replace('~', '-')
        output_path = f'{output_dir}/{title}.pdf'

        # Skip already downloaded files
        if os.path.exists(output_path):
            continue
            
        pdf_url = f'https://openreview.net/pdf?id={submission.forum}'
        response = download_with_retry(pdf_url)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
        else:
            print(f'Failed to download {title} with status code {response.status_code}')
            num_fails += 1

    print(f'Skipped {num_skips} submissions')
    print(f'Failed {num_fails} submissions')

def download_metadata(conferences, years):
    """
    Download metadata for papers from OpenReview conferences
    
    Args:
        username (str): OpenReview username
        password (str): OpenReview password  
        conferences (list): List of conference names (e.g. ["ICLR", "NeurIPS"])
        years (list): List of years to fetch (e.g. ["2024"])
    
    Returns:
        dict: Dictionary containing submissions and reviews for each venue
    """
    # API V2 client setup
    client = openreview.api.OpenReviewClient(
        baseurl='https://api2.openreview.net',
        username=os.environ['OPENREVIEW_USERNAME'],
        password=os.environ['OPENREVIEW_PASSWORD']
    )

    # Get matching venues
    venues = get_venues(client, conferences, years)
    
    metadata = defaultdict(dict)
    for venue_id in venues:
        try:
            venue_group = client.get_group(venue_id)
            submission_name = venue_group.content['submission_name']['value']
            submissions = client.get_all_notes(invitation=f'{venue_id}/-/{submission_name}', details='replies')
            review_name = venue_group.content['review_name']['value']
            reviews=[openreview.api.Note.from_json(reply) for s in submissions for reply in s.details['replies'] if f'{venue_id}/{submission_name}{s.number}/-/{review_name}' in reply['invitations']]
            if len(reviews)!=0:
                print(f"{venue_id}: Submissions: {len(submissions)}, Reviews - {len(reviews)}")
                metadata[venue_id] = {
                    'submissions': submissions,
                    'reviews': reviews
                }
        except:
            pass

    return metadata


if __name__ == "__main__":
    metadata = download_metadata(conferences=["NeurIPS"], years=["2024"])
    download_PDFs(metadata)
