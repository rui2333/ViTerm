window.text2speech = function(text){
  var msg = new SpeechSynthesisUtterance(text);
  window.speechSynthesis.speak(msg);
}
