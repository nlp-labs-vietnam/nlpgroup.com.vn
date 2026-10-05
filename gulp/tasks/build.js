var gulp   = require('gulp');
var config = require('../config');

gulp.task('build', gulp.series(
    function setBuildEnv(done) {
        config.setEnv('production');
        config.logEnv();
        done();
    },
    'clean',
    'sprite:svg',
    'svgo',
    'sass',
    'pug',
    'js',
    'copy'
));

gulp.task('build:dev', gulp.series(
    function setDevEnv(done) {
        config.setEnv('development');
        config.logEnv();
        done();
    },
    'clean',
    'sprite:svg',
    'svgo',
    'sass',
    'pug',
    'js',
    'copy'
));
