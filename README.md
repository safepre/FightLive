# FightLive 

Stay updated with the latest UFC fight results and scorecards directly in your Discord server! 

FightLive is a streamlined tool that fetches live updates from @UFCNews on twitter and delivers them in an engaging format using Discord webhooks.


<img width="559" alt="Screenshot 2024-10-05 at 1 20 29 AM" src="https://github.com/user-attachments/assets/7e012935-27ba-4192-a623-2824b9baa4c1">

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/ufc-fight-tracker.git
   cd ufc-fight-tracker
   ```

2. **Set Up Environment Variables**
   
   Create a `.env` file in the root directory and add the following:
   ```
   WEBHOOK_URL=your_discord_webhook_url
   AUTH_TOKEN=your_twitter_auth_token
   X_ACCOUNT=official_ufc_account
   ```
3. **Install dependencies**
   ```bash  
   pip3 install -r requirements.txt
   ```
6. **Run Program**
   ```bash
   python3 run.py
   ```

