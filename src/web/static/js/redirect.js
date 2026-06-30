const redirectTimerSpan = document.getElementById("redirectTimerSeconds");
const timerUnitSpan = document.getElementById("redirectTimerUnit");

function setTimer() {
  const curSeconds = redirectTimerSpan.innerHTML;
  console.log(curSeconds);

  if (curSeconds < 1) {
    clearInterval(setTimer);
    return;
  }

  secondsNew = curSeconds - 1;
  redirectTimerSpan.innerHTML = secondsNew;
  if (secondsNew == 1) {
    timerUnitSpan.innerHTML = "second";
  }
}

window.addEventListener("load", () => {
  setInterval(setTimer, 1000);
});
