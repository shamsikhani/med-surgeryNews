# RosettaNews

RosettaNews is an AI-powered news aggregation system that automatically scrapes news articles from any website, translates them to English, summarizes the content, and delivers it via email. Built with CrewAI, it uses a team of AI agents to process and curate news content.

## Features

- 🌐 **Universal News Scraping**: Can scrape news from any website regardless of language
- 🔄 **Automatic Translation**: Translates news content to English
- 📝 **Smart Summarization**: Creates concise 2-3 paragraph summaries while maintaining the original tone
- 📧 **Email Delivery**: Sends formatted news digests to specified recipients
- 🤖 **AI-Powered Editing**: Ensures journalistic standards and readability

## Prerequisites

- Python 3.10 or higher
- OpenAI API key
- Serper API key (for web search capabilities)
- Resend API key (for email delivery)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/felixmd/rosetta_news.git
cd RosettaNews
```

2. Create and activate a virtual environment:
```bash
python -m venv .rnews
source .rnews/bin/activate  # On Windows: .rnews\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file with your API keys:
```env
OPENAI_API_KEY=your_openai_key
SERPER_API_KEY=your_serper_key
RESEND_API_KEY=your_resend_key
EMAIL_RECIPIENTS=recipient1@example.com,recipient2@example.com
```

## Usage

1. Configure your target news website in `news_manager.py`:
```python
url = "https://your-news-website.com/news"
```

2. Run the news aggregator:
```bash
python news_manager.py
```

The system will:
1. Scrape the latest news articles
2. Translate them to English
3. Generate summaries
4. Send a formatted email digest to specified recipients

## Project Structure

```
RosettaNews/
├── agents/
│   └── news_reader.py     # AI agent definitions
├── Gateway/
│   └── emailGateway.py    # Email handling
├── config.py              # Configuration settings
├── news_manager.py        # Main application
└── requirements.txt       # Dependencies
```

## How It Works

RosettaNews uses a crew of AI agents:

1. **Press Bureau Agent**: 
   - Scrapes news articles
   - Translates content
   - Generates summaries

2. **Editor Agent**:
   - Reviews content quality
   - Ensures neutral tone
   - Maintains journalistic standards

## Configuration

### Email Settings

Modify email settings in `Gateway/emailGateway.py`:
```python
"from": "Your News <news@yourdomain.com>",
"subject": "Your Custom Subject"
```

### News Source

Update the news source in `config.py`:
```python
NEWS_URL: str = "https://your-news-website.com"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [CrewAI](https://www.crewai.com/)
- Email delivery powered by [Resend](https://resend.com/)
- Web search capabilities by [Serper](https://serper.dev/) 