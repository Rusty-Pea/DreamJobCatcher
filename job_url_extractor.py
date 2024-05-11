import sys
import os
from anthropic import Anthropic

def extract_job_urls(file_name):
    # Read the content from the file
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()

    # Initialize the Anthropic client
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    # Define the prompt for extracting job URLs
    prompt = f"Please extract the job URLs from the following content:\n\n{content}\n\nJob URLs:"

    # Send the prompt to the Claude model using the Anthropic library
    response = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="claude-3-opus-20240229",
    )

    # Extract the job URLs from the response
    job_urls = response.content.strip()

    # Generate the output file name
    output_file_name = f"job_urls_{file_name}"

    # Save the job URLs to the output file
    with open(output_file_name, 'w', encoding='utf-8') as file:
        file.write(job_urls)

    print(f"Job URLs saved to {output_file_name}")

# Check if the script is being run directly
if __name__ == '__main__':
    # Get the file name from the command line argument
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        if os.path.isfile(file_name):
            extract_job_urls(file_name)
        else:
            print(f"File not found: {file_name}")
    else:
        print("Please provide a file name as a command line argument.")