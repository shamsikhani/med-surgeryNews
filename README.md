# Medical & Surgery News

An AI-powered medical and surgical news aggregator that delivers curated, accurate, and timely updates from the healthcare world directly to your inbox.

## Features

- Automated scraping of reliable medical news sources
- AI-powered content curation and summarization
- Expert medical review and fact-checking
- Professional medical editing for clarity
- Daily email digest of the latest medical and surgical developments

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

## Environment Variables

Create a `.env` file with the following variables:
```
SERPER_API_KEY=your_serper_api_key
RESEND_API_KEY=your_resend_api_key
OPENAI_API_KEY=your_openai_api_key
EMAIL_RECIPIENTS=comma,separated,email,addresses
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/medical-surgery-news.git
cd medical-surgery-news
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`

4. Run the application:
```bash
python news_manager.py
```

## Security

- The `.env` file is included in `.gitignore` to protect sensitive information
- API keys and email addresses are securely handled using environment variables

## License

MIT License