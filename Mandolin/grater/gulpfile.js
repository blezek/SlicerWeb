/*
  install:
  npm install --save-dev gulp gulp-concat gulp-notify gulp-cache gulp-livereload tiny-lr gulp-util express
  */


var gulp = require('gulp'),
    concat = require('gulp-concat'),
    notify = require('gulp-notify'),
    cache = require('gulp-cache'),
    refresh = require('gulp-livereload'),
    livereload = require('gulp-livereload'),
    lr = require('tiny-lr'),
    server = lr();

var js = ['lib/js/**/*.js', 'js/**/*.js']
var assets = ['assets/**']
var css = ['css/**/*.css']



var all = [].concat ( js, assets, css )

gulp.task('build', function() {
    gulp.src(js)
    .pipe(concat('grater.js'))
    .pipe(gulp.dest('../docroot/js'))
    .pipe(refresh(server));

    gulp.src(assets)
    .pipe(gulp.dest('../docroot'))
    .pipe(refresh(server));

    gulp.src(css)
    .pipe(concat('grater.css'))
    .pipe(gulp.dest('../docroot/css'))
    .pipe(refresh(server));
});

gulp.task('lr-server', function() {
  server.listen(35729, function(err) {
    if (err) return console.log(err);
  });
});

gulp.task('default', ['lr-server', 'foundation', 'build'], function() {
  gulp.watch(all, ['build']);
})


// Build Foundation
gulp.task('foundation', function() {
  var foundation = ['bower_components/foundation/js/vendor/jquery.js', 'bower_components/foundation/js/vendor/**/*.js', 'bower_components/foundation/js/foundation.js']
  gulp.src(foundation).pipe(concat('foundation.js')).pipe(gulp.dest('../docroot/js'));

  var css = ['bower_components/foundation/css/foundation.css', 'bower_components/foundation/css/normalize.css'];
  gulp.src(css)
  .pipe(gulp.dest('../docroot/css'))
})

