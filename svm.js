var svm = require('node-svm');
var training = require('./processed_trained_data.json');
var testing = require('./processed_test_data.json');
// var emotion_model = require('./emotion_classifier.json');

// var clf = svm.restore(emotion_model);

// initialize a new predictor
var clf = new svm.EpsilonSVR();

var training_data = [];
training.data.forEach(function(data){
  var tempArr = [[]];
  tempArr[0] = data[0];
  data[1].forEach(function(val, index){
    if(val == 1){
      tempArr.push(index+1);
    }
  });

  training_data.push(tempArr);
});

var testing_data = [];
testing.data.forEach(function(data){
  var tempArr = [[]];
  tempArr[0] = data[0];
  data[1].forEach(function(val, index){
    if(val == 1){
      tempArr.push(index+1);
    }
  });

  testing_data.push(tempArr);
});


clf.train(training_data).done(function () {
    // predict things
    testing_data.forEach(function(ex){
        var prediction = clf.predictSync(ex[0]);
        console.log('prediction: %d, real: %d', prediction, ex[1]);
    });
});

var self = {};

self.predict = function(input){
  var prediction = clf.predictSync(input);
  return prediction;
}

module.exports = self;
