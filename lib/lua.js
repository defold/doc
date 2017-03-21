/*
Language: Lua
Author: Andrew Fedorov <dmmdrs@mail.ru>
Category: scripting
*/

module.exports = {
  lua: function(hljs) {
      var OPENING_LONG_BRACKET = '\\[=*\\[';
      var CLOSING_LONG_BRACKET = '\\]=*\\]';
      var LONG_BRACKETS = {
        begin: OPENING_LONG_BRACKET, end: CLOSING_LONG_BRACKET,
        contains: ['self']
      };
      var COMMENTS = [
        hljs.COMMENT('--(?!' + OPENING_LONG_BRACKET + ')', '$',
            {
              relevance : 0,
              contains : [{
                className : 'doctag',
                begin : '@[A-Za-z]+'
              }]
            }
          ),
        hljs.COMMENT(
          '--' + OPENING_LONG_BRACKET,
          CLOSING_LONG_BRACKET,
          {
            contains: [LONG_BRACKETS],
            relevance: 10
          }
        )
      ];
      return {
        lexemes: hljs.UNDERSCORE_IDENT_RE,
        keywords: {
          literal: "true false nil",
          keyword: "and break do else elseif end for goto if in local not or repeat return then until while",
          built_in:
            //Metatags and globals:
            '_G _ENV _VERSION __index __newindex __mode __call __metatable __tostring __len ' +
            '__gc __add __sub __mul __div __mod __pow __concat __unm __eq __lt __le assert ' +
            //Standard methods and properties:
            'collectgarbage dofile error getfenv getmetatable ipairs load loadfile loadstring' +
            'module next pairs pcall print rawequal rawget rawset require select setfenv' +
            'setmetatable tonumber tostring type unpack xpcall arg self ' +
            // Defold builtins
            'base bit builtins camera collectionfactory collectionproxy coroutine crash debug facebook factory go gui http iac iap image io json label math model msg os package particlefx physics push render resource sound spine sprite string sys table tilemap vmath webview window zlib'
        },
        contains: COMMENTS.concat([
          {
            className: 'function',
            beginKeywords: 'function', end: '\\)',
            contains: [
              hljs.inherit(hljs.TITLE_MODE, {begin: '([_a-zA-Z]\\w*\\.)*([_a-zA-Z]\\w*:)?[_a-zA-Z]\\w*'}),
              {
                className: 'params',
                begin: '\\(', endsWithParent: true,
                contains: COMMENTS
              }
            ].concat(COMMENTS)
          },
          hljs.C_NUMBER_MODE,
          hljs.APOS_STRING_MODE,
          hljs.QUOTE_STRING_MODE,
          {
            className: 'string',
            begin: OPENING_LONG_BRACKET, end: CLOSING_LONG_BRACKET,
            contains: [LONG_BRACKETS],
            relevance: 5
          }
        ])
    };
}}
