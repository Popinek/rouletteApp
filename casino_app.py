from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key for production


# Set initial bankroll and stats when starting the game
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            starting_bankroll = float(request.form['bankroll'])
            session['bankroll'] = starting_bankroll
            session['starting_bankroll'] = starting_bankroll
            session['total_wins'] = 0  # Track total money won
            session['total_losses'] = 0  # Track total money lost
            session['win_count'] = 0  # Track total win count
            session['loss_count'] = 0  # Track total loss count
            return redirect(url_for('play'))
        except ValueError:
            return render_template('home.html', error="Please enter a valid number.")
    return render_template('home.html')


# Game route where the user can place bets
@app.route('/play', methods=['GET', 'POST'])
def play():
    if 'bankroll' not in session:
        return redirect(url_for('home'))

    bankroll = session['bankroll']
    result = None
    win = False

    if request.method == 'POST':
        # Player's chosen number to bet on
        player_number = int(request.form['number'])

        # Spin the roulette wheel (random number between 0 and 36 for European roulette)
        roulette_number = random.randint(0, 36)

        # Check if the player wins (payout is 35:1)
        if player_number == roulette_number:
            winnings = 35  # Win $35 for a $1 bet
            bankroll += winnings
            session['total_wins'] += winnings
            session['win_count'] += 1
            result = f"Congratulations! You won! The ball landed on {roulette_number}."
            win = True
        else:
            bankroll -= 1  # Lose $1 for a losing bet
            session['total_losses'] += 1
            session['loss_count'] += 1
            result = f"You lost! The ball landed on {roulette_number}."

        # Update bankroll in session
        session['bankroll'] = bankroll

    # Calculate current winnings/losses and luck status
    net_gain = bankroll - session['starting_bankroll']  # Net gain/loss
    expected_outcome = session['starting_bankroll'] * (1 - 0.027) ** (session['win_count'] + session['loss_count'])
    luck_status = "lucky" if bankroll > expected_outcome else "unlucky"

    return render_template('play.html', bankroll=bankroll, result=result, win=win,
                           net_gain=net_gain, total_wins=session['total_wins'],
                           total_losses=session['total_losses'], win_count=session['win_count'],
                           loss_count=session['loss_count'], luck_status=luck_status)


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
