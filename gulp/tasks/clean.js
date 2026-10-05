var gulp   = require('gulp');
var del    = require('del');
var log    = require('fancy-log');
var colors = require('ansi-colors');
var config = require('../config');

gulp.task('clean', function() {
    return del([
        config.dest.root
    ]).then(function(paths) {
        log('Deleted:', colors.magenta(paths.join('\n')));
    });
});
