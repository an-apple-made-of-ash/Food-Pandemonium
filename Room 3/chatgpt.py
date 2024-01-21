import openai
import time
import tiktoken  # Make sure to install this library

# DUMMY KEYWORDS

# Set your company's ChatGPT API key and URL here
company_api_key = "981bdca6dae44b78a930541b4577f696"
company_api_url = "https://dso-ie-openai.openai.azure.com/"

# Ensure the company's ChatGPT API key is used directly
openai.api_key = company_api_key

def estimate_cost(query, context, output, model='gpt-4'):
    '''
    Estimate cost of your query to GPT4
    '''
    cost_dict = {'gpt-4': {
                    'input': 0.03, 
                    'output': 0.06
                 },
                 'gpt-3.5': {
                    'input': 0.001,
                    'output': 0.002 
                 }
                }
    enc = tiktoken.encoding_for_model(model)
    
    # Ensure context, query, and output are strings
    context_str = str(context)
    query_str = str(query)
    output_str = str(output)

    cost = ((len(enc.encode(context_str + query_str)) / 1000) * cost_dict[model]['input']) + ((len(enc.encode(output_str)) / 1000) * cost_dict[model]['output'])

    print('Cost of query: USD$ {}'.format(round(cost, 2)))


def ask_company_chatgpt(prompt, model='gpt-4', max_tokens=256):
    # Call the company's ChatGPT API
    openai.api_type = "azure"
    openai.api_version = "2023-05-15"
    openai.api_base = "https://dso-ie-openai.openai.azure.com/"
    openai.api_key = "981bdca6dae44b78a930541b4577f696"
    if model == 'gpt-4':
        azure_oai_model = "dsogpt4" 
    else:
        azure_oai_model = "dsochatgpt35"

    start = time.time()
    response = openai.ChatCompletion.create(
                engine=azure_oai_model,
                temperature=0,
                max_tokens=max_tokens,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": prompt}
                ]
            )
    end = time.time()
    output = response.choices[0].message.content
    
    print('Answer:\n{}\n'.format(output))
    print('Processing time: {} s'.format(round(end-start, 2)))
    estimate_cost(prompt, prompt, output, model)

def main():
    # OCR on the image
    prompt = "Pretend you are an annoyed resident. Give me one very rude sentence expressing annoyance towards the delivery man for being slow"

    # Ask Company's ChatGPT for truthfulness label
    insult = ask_company_chatgpt(prompt)
    #print("\nTruthfulness Label Table:")
    #print(truthfulness_label_table)

    # Estimate cost
    estimate_cost(prompt, prompt, insult, model='gpt-4')

if __name__ == "__main__":
    main()

