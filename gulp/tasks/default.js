var gulp   = require('gulp');
var config = require('../config');

gulp.task('default', gulp.series(
    'build:dev',
    gulp.parallel('watch', 'server')
));
