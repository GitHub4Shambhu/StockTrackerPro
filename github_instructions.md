# Moving Your Replit Project to GitHub

Follow these steps to move your Replit project to GitHub:

1. Create a GitHub account:
   - If you don't have a GitHub account, go to https://github.com and sign up for a free account.

2. Create a new repository on GitHub:
   - Click on the "+" icon in the top right corner of GitHub and select "New repository".
   - Choose a name for your repository (e.g., "StockTrackerPro").
   - Set the repository to "Public" or "Private" based on your preference.
   - Do not initialize the repository with a README, .gitignore, or license.
   - Click "Create repository".

3. Initialize git in your Replit project:
   - Open the Replit shell (if not already open).
   - Run the following commands:
     ```
     git init
     git add .
     git commit -m "Initial commit"
     ```

4. Add your GitHub repository as a remote:
   - On the GitHub repository page, copy the URL of your repository.
   - In the Replit shell, run:
     ```
     git remote add origin YOUR_GITHUB_REPO_URL
     ```
   Replace `YOUR_GITHUB_REPO_URL` with the URL you copied.

5. Push your code to GitHub:
   - In the Replit shell, run:
     ```
     git push -u origin master
     ```
   - If prompted, enter your GitHub username and password (or personal access token).

6. Verify the push:
   - Go to your GitHub repository page and refresh.
   - You should see all your project files there.

7. Set up GitHub credentials in Replit (optional, for easier future pushes):
   - In Replit, go to the "Secrets" tab (lock icon in the left sidebar).
   - Add two new secrets:
     - Key: GITHUB_USERNAME, Value: Your GitHub username
     - Key: GITHUB_TOKEN, Value: Your GitHub personal access token
   - To create a personal access token, go to GitHub Settings > Developer settings > Personal access tokens > Generate new token.

Now your Replit project is connected to GitHub. You can make changes in Replit and push them to GitHub using git commands in the Replit shell.

Remember to keep your GitHub credentials and personal access tokens secure and never share them publicly.
