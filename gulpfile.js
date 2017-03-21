// Node modules
var gulp = require('gulp');
var watch = require('gulp-watch');
var plumber = require('gulp-plumber');
var gutil = require('gulp-util');
var tap = require('gulp-tap');
var hljs = require('highlight.js')
var server = require('gulp-server-livereload');
var wrapper = require('gulp-wrapper');
var sass = require('gulp-sass');
var minify = require('gulp-cssnano');
var del = require('del');
var mkdirp = require('mkdirp');
var slugify = require('slugify');
var hljs = require('highlight.js');

var print = require('gulp-print');

var markdown = require('markdown-it');
var md_attrs = require('markdown-it-attrs');
var md_container = require('markdown-it-container');
var md_deflist = require('markdown-it-deflist')
var md_sub = require('markdown-it-sub');
var md_sup = require('markdown-it-sup');

// hljs lua highlight patched
var lua = require('./lib/lua');
hljs.registerLanguage('lua', lua.lua);

md = new markdown({
  html: true,
  xhtmlOut: true,
  breaks: false,
  langPrefix: 'language-',
  linkify: true,
  typographer: true,
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        var hl = hljs.highlight(lang, str).value;
        // Callouts hack!
        return hl.replace(/-- &lt;([0-9]+)&gt;/g, '<span class="callout" data-pseudo-content="$1"></span>');
      } catch (__) {}
    }
    return ''; // use external default escaping
  }});

md.use(md_deflist);
md.use(md_attrs);
md.use(md_sub);
md.use(md_sup);
md.use(md_container, 'sidenote', {});
md.use(md_container, 'important', {});

function slugname(str) {
    return '_' + slugify(str, '_').toLowerCase();
}

// Add anchors to all headings.
md.renderer.rules.heading_open = function (tokens, idx, options, env, self) {
    var tag = tokens[idx].tag;
    var slug = slugname(tokens[idx + 1].content);
    return '<a name="' + slug + '" class="anchor"></a>' +
            '<' + tag + '>';
};

md.renderer.rules.heading_close = function (tokens, idx, options, env, self) {
    var slug = slugname(tokens[idx - 1].content);
    var tag = tokens[idx].tag;
    if (tag == 'h2' || tag == 'h3')
        return '<a href="#' + slug + '"><span class="anchor-link"></span></a>\n'
                + '</' + tag + '>';
    else
        return '</' + tag + '>';
};

function markdownToHtml(file) {
    var result = md.render(file.contents.toString());
    file.contents = new Buffer(result);
    file.path = gutil.replaceExtension(file.path, '.html');
    return;
}

// Watch for changes in md files and compile new html
gulp.task('watch', function () {

    mkdirp('build');

    gulp.src('build')
        .pipe(server({
            livereload: true,
            open: true,

            directoryListing: {
                enable: true,
                path: 'build'
            }
        }));

    watch(['docs/**/*.sass'], function () {
        gulp.start('sass');
    });

    gulp.start('sass');

    gulp.src('docs/**/images/**/*.*')
        .pipe(watch('docs/**/images/**/*.*'))
        .pipe(gulp.dest("build"));

    // Inject some styling html for the preview. The built htmls are clean.
    var inj_head = '<html><head><link type="text/css" rel="stylesheet" href="/defold-md.css"></head><body>\n';
    inj_head += '<div class="documentation">';
    var inj_foot = '</div></body></html>\n';

    return gulp.src('docs/**/*.md')
        .pipe(watch('docs/**/*.md'))
        .pipe(tap(markdownToHtml))
        .pipe(wrapper({
            header: inj_head,
            footer: inj_foot,
            }))
        .pipe(print())
        .pipe(gulp.dest("build"));
});

gulp.task('clean', [], function() {
    return del(['build']);
});

gulp.task('sass', [], function() {
    gulp.src('docs/sass/defold-md.sass')
        .pipe(plumber())
        .pipe(sass())
        .pipe(minify())
        .pipe(gulp.dest('build'))
});
