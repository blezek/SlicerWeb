/*
  install:
  npm install --save-dev gulp gulp-concat gulp-notify gulp-cache gulp-livereload tiny-lr gulp-util express gulp-browserify
  */


var gulp = require('gulp'),
    concat = require('gulp-concat'),
    notify = require('gulp-notify'),
    cache = require('gulp-cache'),
    refresh = require('gulp-livereload'),
    livereload = require('gulp-livereload'),
    uglify = require('gulp-uglify'),
    lr = require('tiny-lr'),
    server = lr();

var js = ['js/**/*.js']
var assets = ['assets/**']
var css = ['css/**/*.css']



var all = [].concat ( js, assets, css )

gulp.task('build', function() {
    gulp.src(js)
    // .pipe(concat('grater.js'))
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

gulp.task('default', ['watch']);{}
gulp.task('watch', ['lr-server', 'vendor', 'build'], function() {
  gulp.watch(all, ['build']);
})



gulp.task('vendor', function() {
  
  // Build Foundation
  var foundation = ['bower_components/foundation/js/vendor/jquery.js',
  'bower_components/foundation/js/vendor/**/*.js',
  'bower_components/foundation/js/foundation.js',
  'bower_components/modernizr/modernizr.js',
  'bower_components/requirejs/require.js']
  gulp.src(foundation).pipe(gulp.dest('../docroot/js'));

  var css = ['bower_components/foundation/css/foundation.css', 'bower_components/foundation/css/normalize.css'];
  gulp.src(css)
  .pipe(gulp.dest('../docroot/css'))

  var js = [
  'bower_components/underscore/underscore.js',
  // 'bower_components/angular/angular.js',
  'bower_components/backbone/backbone.js',
  'lib/js/dat.gui.js',
  'lib/js/xtk.js',
  'bower_components/angularAMD/ngload.js',
  'bower_components/angularAMD/angularAMD.js'
  ]
  gulp.src(js)
  // .pipe(concat('vendor.js'))
  // .pipe(uglify({outputSourceMap:true}))
  .pipe(gulp.dest('../docroot/js'))

  gulp.src("lib/js/X/**/*.js").pipe(gulp.dest('../docroot/js/X'))

})

