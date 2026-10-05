var gulp   = require('gulp');
var server = require('browser-sync').create();
var log    = require('fancy-log');
var colors = require('ansi-colors');
var argv   = require('minimist')(process.argv.slice(2));
var config = require('../config');

gulp.task('server', function(done) {
    server.init({
        server: {
            baseDir: !config.production ? [config.dest.root, config.src.root] : config.dest.root,
            directory: false,
            serveStaticOptions: {
                extensions: ['html']
            }
        },
        files: [
            config.dest.html + '/*.html',
            config.dest.css + '/*.css',
            config.dest.img + '/**/*'
        ],
        port: argv.port || 3000,
        logLevel: 'info',
        logConnections: false,
        logFileChanges: true,
        open: true,
        notify: false,
        ghostMode: false,
        online: true,
        tunnel: argv.tunnel || null
    });
    done();
});

module.exports = server;
