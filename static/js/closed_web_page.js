const countdown = document.querySelector('.countdown');
const daysSpan = countdown.querySelector('#days');
const hoursSpan = countdown.querySelector('#hours');
const minutesSpan = countdown.querySelector('#minutes');
const secondsSpan = countdown.querySelector('#seconds');

function updateCountdown() {
  const now = new Date();
  const targetDate = new Date('2024-04-27T23:00:00'); // Update with your actual launch date and time (ISO 8601 format)

  // Calculate the time difference in milliseconds
  const timeLeft = targetDate - now;

  if (timeLeft < 0) {
    clearInterval(intervalId);
    // Display a message indicating the launch has occurred
    countdown.innerHTML = 'Launched!';
    return;
  }

  //const days = Math.max(Math.floor(timeLeft / (1000 * 60 * 60 * 24)), 0);
  const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

  // Display remaining time
  //daysSpan.innerHTML = days === 0 ? '0 days' : days;
  hoursSpan.innerHTML = hours.toString().padStart(2, '0') + " Hours";
  minutesSpan.innerHTML = minutes.toString().padStart(2, '0') + " Minutes";
  secondsSpan.innerHTML = seconds.toString().padStart(2, '0') + " Seconds";
}

let intervalId = setInterval(updateCountdown, 1000);
