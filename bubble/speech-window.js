// Speech bubble window: main calls window.setSpeech(text) / window.clearSpeech()
(function () {
  const el = document.getElementById("bubble");
  window.setSpeech = (text) => {
    el.textContent = text;
    el.classList.remove("show");
    void el.offsetWidth;
    el.classList.add("show");
  };
  window.clearSpeech = () => el.classList.remove("show");
})();
