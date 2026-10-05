var gulp = require('gulp');
var include = require('gulp-include');
var config = require('../config');
var browserSync = require('browser-sync');
var babel = require('gulp-babel');
var reload = browserSync.reload;

gulp.task('js', function() {
    return gulp.src(config.src.js + '/**/*.js')
        .pipe(include())
        .pipe(babel())
        .pipe(gulp.dest(config.dest.js + '/'))
        .pipe(reload({ stream: true }));
});

gulp.task('js:watch', function() {
    gulp.watch(config.src.js + '/*', gulp.series('js'));
});
