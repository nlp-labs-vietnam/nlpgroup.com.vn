var gulp   = require('gulp');
var config = require('../config');

gulp.task('watch', gulp.parallel(
    'copy:watch',
    'pug:watch',
    'sprite:svg:watch',
    'svgo:watch',
    'js:watch',
    'sass:watch'
));
