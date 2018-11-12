// Node modules
var gulp = require('gulp')
var watch = require('gulp-watch')
var plumber = require('gulp-plumber')
var preservetime = require('gulp-preservetime')
var gutil = require('gulp-util')
var tap = require('gulp-tap')
var jsonlint = require('gulp-jsonlint')
var server = require('gulp-server-livereload')
var sass = require('gulp-sass')
var minify = require('gulp-cssnano')
var del = require('del')
var path = require('path')
var mkdirp = require('mkdirp')
var slugify = require('slugify')
var through = require('through2')
var File = require('vinyl')
var hljs = require('highlight.js')
var print = require('gulp-print')
var frontmatter = require('front-matter')
var markdown = require('markdown-it')
var md_attrs = require('markdown-it-attrs')
var md_container = require('markdown-it-container')
var md_deflist = require('markdown-it-deflist')
var md_sub = require('markdown-it-sub')
var md_sup = require('markdown-it-sup')
var md_katex = require('markdown-it-katex')
var hercule = require('hercule')

// hljs lua highlight patched
var lua = require('./lib/lua')
hljs.registerLanguage('lua', lua.lua)

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
        var hl = hljs.highlight(lang, str).value
        // Callouts hack!
        // replaces "-- [1]", "// [1]" and "-- <1>" and "// <1>" with a span
        // callouts only work if the highlighter kicks in.
        var exp = /(?:\-\-|\/\/|#) (?:\[|&lt;)([0-9]+)(?:\]|&gt;)/g
        return hl.replace(exp,
          '<span class="callout" data-pseudo-content="$1"></span>')
      } catch (__) {
      }
    }
    return '' // use external default escaping
  },
})

md.use(md_deflist)
md.use(md_attrs)
md.use(md_sub)
md.use(md_sup)
md.use(md_katex)
md.use(md_container, 'sidenote', {render: rendernote})
md.use(md_container, 'important', {render: rendernote})

// Notes are rendered as two divs so they can be styled right
function rendernote (tokens, idx) {
  if (tokens[idx].nesting === 1) {
    // opening tag
    var type = tokens[idx].info.trim().match(/^(\w+).*$/)[1]
    return '<div class="note ' + type +
      '"><div class="note-icon"></div><div class="note-content">'
  } else {
    // closing tag
    return '</div></div>\n'
  }
}

function slugname (str) {
  return '_' + slugify(str, '_').toLowerCase()
}

// Add anchors to all headings.
md.renderer.rules.heading_open = function (tokens, idx, options, env, self) {
  var tag = tokens[idx].tag
  var title = tokens[idx + 1].content
  var slug = slugname(title)
  // Add TOC entry
  if (!('toc' in env)) {
    env.toc = []
  }
  var level = tag.match(/^h(\d+)$/)[1]
  env.toc.push({entry: title, slug: slug, level: level})
  return '<div id="' + slug + '" class="anchor"></div>' +
    '<' + tag + '>'
}

md.renderer.rules.heading_close = function (tokens, idx, options, env, self) {
  var slug = slugname(tokens[idx - 1].content)
  var tag = tokens[idx].tag
  if (tag == 'h2' || tag == 'h3')
    return '<a href="#' + slug + '"><span class="anchor-link"></span></a>\n'
      + '</' + tag + '>'
  else
    return '</' + tag + '>'
}

// Images.
md.renderer.rules.image = function (tokens, idx, options, env, self) {
  var token = tokens[idx]

  if ('imgurl' in env) {
    // Rewrite src and srcset
    // TODO: check if an url is absolute (leave as is) or relative (rewrite).
    var src = token.attrs[token.attrIndex('src')][1]
    token.attrs[token.attrIndex('src')][1] = env.imgurl + '/' + src

    if (token.attrs[token.attrIndex('srcset')]) {
      // TODO: srcset should be properly split and the url part should be
      // rewritten.
      var srcset = token.attrs[token.attrIndex('srcset')][1]
      token.attrs[token.attrIndex('srcset')][1] = env.imgurl + '/' +
        srcset
    }
  }
  // Set alt attribute
  token.attrs[token.attrIndex('alt')][1] = self.renderInlineAsText(
    token.children, options, env)

  return self.renderToken(tokens, idx, options)
}

var HTML_ESCAPE_TEST_RE = /[&<>"]/
var HTML_ESCAPE_REPLACE_RE = /[&<>"]/g
var HTML_REPLACEMENTS = {
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
}

function replaceUnsafeChar (ch) {
  return HTML_REPLACEMENTS[ch]
}

function escapeHtml (str) {
  if (HTML_ESCAPE_TEST_RE.test(str)) {
    return str.replace(HTML_ESCAPE_REPLACE_RE, replaceUnsafeChar)
  }
  return str
}

// Fence code blocks
md.renderer.rules.fence = function (tokens, idx, options, env, self) {
  var token = tokens[idx],
    info = token.info ? decodeURI(token.info).trim() : '',
    langName = '',
    highlighted, i, tmpAttrs, tmpToken

  if (info) {
    langName = info.split(/\s+/g)[0]
  }

  if (options.highlight) {
    highlighted = options.highlight(token.content, langName) ||
      escapeHtml(token.content)
  } else {
    highlighted = escapeHtml(token.content)
  }

  if (highlighted.indexOf('<pre') === 0) {
    return highlighted + '\n'
  }

  var id = 'codesnippet_' + idx
  var copy = '<button class="copy-to-clipboard" data-clipboard-target="#' +
    id + '"><span class="icon-clipboard"></span></button>'

  // If language exists, inject class gently, without modifying original token.
  // May be, one day we will add .clone() for token and simplify this part, but
  // now we prefer to keep things local.
  if (info) {
    i = token.attrIndex('class')
    tmpAttrs = token.attrs ? token.attrs.slice() : []

    if (i < 0) {
      tmpAttrs.push(['class', options.langPrefix + langName])
    } else {
      tmpAttrs[i][1] += ' ' + options.langPrefix + langName
    }

    // Fake token just to render attributes
    tmpToken = {
      attrs: tmpAttrs,
    }

    return '<pre>' + '<code id="' + id + '"' + self.renderAttrs(tmpToken) +
      '>'
      + highlighted
      + '</code>' + copy + '</pre>\n'
  }

  return '<pre>' + '<code id="' + id + '"' + self.renderAttrs(token) + '>'
    + highlighted
    + '</code>' + copy + '</pre>\n'
}

// Output preview html documents
function markdownToPreviewHtml (file) {
  var data = frontmatter(file.contents.toString())
  // Inject some styling html for the preview. The built htmls are clean.
  var head = '<!DOCTYPE html><html><head><link type="text/css" rel="stylesheet" href="/preview-md.css">' +
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.7.1/katex.min.css" integrity="sha384-wITovz90syo1dJWVh32uuETPVEtGigN07tkttEqPv+uR2SE/mbQcG7ATL28aI9H0" crossorigin="anonymous">' +
    '</head><body>\n'
  head += '<div class="documentation">'
  var foot = '</div></body></html>\n'
  var html = head + md.render(data.body) + foot
  file.contents = Buffer.from(html)
  file.path = gutil.replaceExtension(file.path, '.html')
}

var img_url = 'https://storage.googleapis.com/defold-doc'
//var img_url = '/_ah/gcs/defold-doc'; // local dev-server

// Build document json for storage
function markdownToJson (file) {
  var name = path.relative(file.base, file.path)
  // Needs language for static image url:s
  var m = name.match(/^(\w+)[/](\w+)[/].*$/)
  var lang = m[1]
  var doctype = m[2]
  var data = frontmatter(file.contents.toString())
  var env = {imgurl: img_url + '/' + lang + '/' + doctype}
  data.html = md.render(data.body, env)
  data.toc = env.toc
  file.contents = Buffer.from(JSON.stringify(data))
  file.path = gutil.replaceExtension(file.path, '.json')
}

// Create a map path -> [lang1, lang2 ...] and add it to the
// languages.json file
function langMap (jsonfile) {
  var langmap = require('./docs/' + jsonfile)
  langmap['filemap'] = {}
  return through.obj(function (file, enc, cb) {
    var fullpath = path.relative(file.base, file.path)
    var m = fullpath.match(/^(\w+)[/](\w+)[/].*$/)
    var lang = m[1]
    var name = path.relative(lang, fullpath)
    if (!langmap['filemap'][name]) {
      langmap['filemap'][name] = []
    }
    langmap['filemap'][name].push(lang)
    cb(null, file)
  }, function (cb) {
    f = new File({
      path: jsonfile,
      contents: Buffer.from(JSON.stringify(langmap)),
    })
    this.push(f)
    cb()
  })
}

// Support for transclusion via :[](file.md) syntax
function gulpHercule () {
  return through.obj(function (file, encoding, callback) {
    if (file.isNull()) {
      return callback(null, file)
    }

    if (file.isBuffer()) {
      var options = {'source': file.path}
      hercule.transcludeString(file.contents.toString(encoding), options,
        function (err, output) {
          if (err) {
            // Handle exceptions like dead links
            process.stderr.write(
              'ERROR: ' + err.message + ' (' + err.path + ')\n')
            process.exit(1)
          }
          file.contents = Buffer.from(output)
          return callback(null, file)
        })
    }

    if (file.isStream()) {
      var transcluder = new hercule.TranscludeStream(options)
      transcluder.on('error', (err) => {
        // Handle exceptions like dead links
        process.stderr.write(
          'ERROR: ' + err.message + ' (' + err.path + ')\n')
        process.exit(1)
      })

      file.contents = file.contents.pipe(transcluder)
      return callback(null, file)
    }
  })
}

function clean () {
  return del(['build'])
}

function copyAssets () {
  gulp.src(['docs/assets/**/*.*']).
    pipe(gulp.dest('build/assets')).
    pipe(preservetime())

  return gulp.src(['docs/**/*.{png,jpg,svg,gif,js,zip,js}']).
    pipe(gulp.dest('build')).
    pipe(preservetime())
}

function build () {
  return gulp.src('docs/**/*.md').
    pipe(gulpHercule()).
    pipe(tap(markdownToJson)).
    pipe(langMap('languages.json')).
    pipe(gulp.dest('build')).
    pipe(preservetime())
}

function lintJSON () {
  return gulp.src(['docs/*/*.json']).pipe(jsonlint()).
    pipe(jsonlint.reporter()).
    pipe(gulp.dest('build')).
    pipe(preservetime())
}

function compilePreviewAssets () {
  return gulp.src('docs/**/images/**/*.*').pipe(gulp.dest('build/preview'))
}

function watchAssets () {
  return watch('docs/**/images/**/*.*', compilePreviewAssets)
}

function compilePreviewMarkdown (cb) {
  return gulp.src('docs/**/*.md').
    pipe(gulpHercule()).
    pipe(tap(markdownToPreviewHtml)).
    pipe(print()).
    pipe(gulp.dest('build/preview'))
}

function watchMarkdown () {
  return watch('docs/**/*.md', compilePreviewMarkdown)
}

function compilePreviewSass () {
  return gulp.src('docs/sass/preview-md.sass').
    pipe(plumber()).
    pipe(sass()).
    pipe(minify()).
    pipe(gulp.dest('build/preview'))
}

function watchSass () {
  return watch(['docs/**/*.sass'], compilePreviewSass)
}

function createPreviewDir (cb) {
  mkdirp('build/preview', cb)
}

function serve () {
  return gulp.src('./build/preview').pipe(server({
    livereload: true,
    open: true,
    port: 8989,

    directoryListing: {
      enable: true,
      path: './build/preview',
    },
  }))
}

gulp.task('build', gulp.series(clean, copyAssets, build, lintJSON))
gulp.task('preview-assets', compilePreviewAssets)
gulp.task('preview-md', compilePreviewMarkdown)
gulp.task('sass', compilePreviewSass)

// Watch for changes in md files and compile new html
gulp.task('watch',
  gulp.series(
    createPreviewDir,
    compilePreviewAssets,
    compilePreviewMarkdown,
    compilePreviewSass,
    gulp.parallel(
      serve,
      watchSass,
      watchAssets,
      watchMarkdown,
    ),
  ),
)


