
  // progressbar.js@1.0.0 version is used
// Docs: http://progressbarjs.readthedocs.org/en/1.0.0
var bar_value = 90;
var bar1_value = 30;
var bar2_value = 50;
var bar3_value = 70;
var duration = 4000;
var width = 7;


var bar = new ProgressBar.Circle(container, {
  color: '#fffff',
  // This has to be the same size as the maximum width to
  // prevent clipping
  strokeWidth: 4,
  trailWidth: 7,
  easing: 'easeInOut',
  duration: duration,
  text: {
    autoStyleContainer: false
  },
  from: { color: '#ff0000', width: width },
  to: { color: '#15b213', width: width },
  // Set default step function for all animate calls
  step: function(state, circle) {
    circle.path.setAttribute('stroke', state.color);
    circle.path.setAttribute('stroke-width', state.width);

    var value = Math.round(circle.value() * 100);
    if (value === 0) {
      circle.setText('');
    } else {
      circle.setText(`<center>${(value.toString())}%</center>` + "\nImproved");
    }

  }
});
bar.text.style.color = 'gray';
bar.text.style.fontFamily = '"Raleway", Helvetica, sans-serif';
bar.text.style.fontSize = '3rem';

bar.animate(bar_value / 100);  // Number from 0.0 to 1.0


var bar1 = new ProgressBar.Circle(container1, {
  color: '#fffff',
  // This has to be the same size as the maximum width to
  // prevent clipping
  strokeWidth: 4,
  trailWidth: 7,
  easing: 'easeInOut',
  duration: duration,
  text: {
    autoStyleContainer: false
  },
  from: { color: '#ff0000', width: width },
  to: { color: '#15b213', width: width },
  // Set default step function for all animate calls
  step: function(state, circle) {
    circle.path.setAttribute('stroke', state.color);
    circle.path.setAttribute('stroke-width', state.width);

    var value = Math.round(circle.value() * 100);
    if (value === 0) {
      circle.setText('');
    } else {
      circle.setText(`<center>${(value.toString())}%</center>` + "\nImproved");
    }

  }
});
bar1.text.style.color = 'gray';
bar1.text.style.fontFamily = '"Raleway", Helvetica, sans-serif';
bar1.text.style.fontSize = '3rem';

bar1.animate(bar1_value / 100);  // Number from 0.0 to 1.0

var bar2 = new ProgressBar.Circle(container2, {
  color: '#fffff',
  // This has to be the same size as the maximum width to
  // prevent clipping
  strokeWidth: 4,
  trailWidth: 7,
  easing: 'easeInOut',
  duration: duration,
  text: {
    autoStyleContainer: false
  },
  from: { color: '#ff0000', width: width },
  to: { color: '#15b213', width: width },
  // Set default step function for all animate calls
  step: function(state, circle) {
    circle.path.setAttribute('stroke', state.color);
    circle.path.setAttribute('stroke-width', state.width);

    var value = Math.round(circle.value() * 100);
    if (value === 0) {
      circle.setText('');
    } else {
      circle.setText(`<center>${(value.toString())}%</center>` + "\nImproved");
    }

  }
});
bar2.text.style.color = 'gray';
bar2.text.style.fontFamily = '"Raleway", Helvetica, sans-serif';
bar2.text.style.fontSize = '3rem';

bar2.animate(bar2_value / 100);  // Number from 0.0 to 1.0

var bar3 = new ProgressBar.Circle(container3, {
  color: '#fffff',
  // This has to be the same size as the maximum width to
  // prevent clipping
  strokeWidth: 4,
  trailWidth: 7,
  easing: 'easeInOut',
  duration: duration,
  text: {
    autoStyleContainer: false
  },
  from: { color: '#ff0000', width: width },
  to: { color: '#15b213', width: width },
  // Set default step function for all animate calls
  step: function(state, circle) {
    circle.path.setAttribute('stroke', state.color);
    circle.path.setAttribute('stroke-width', state.width);

    var value = Math.round(circle.value() * 100);
    if (value === 0) {
      circle.setText('');
    } else {
      circle.setText(`<center>${(value.toString())}%</center>` + "\nImproved");
    }

  }
});
bar3.text.style.color = 'gray';
bar3.text.style.fontFamily = '"Raleway", Helvetica, sans-serif';
bar3.text.style.fontSize = '3rem';

bar3.animate(bar3_value / 100);  // Number from 0.0 to 1.0