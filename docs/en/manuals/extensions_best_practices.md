# Best Practices

Writing cross platform code can be difficult, but there are some ways to make it easier to both develop and maintain.
Here we list some ways we at Defold work with cross platform native code and API's.

## C++ code

### Standard Template Libraries - STL

Since the Defold engine doesn't use any STL code, except for some algorithms and math (std::sort, std::upper_bound etc), it may work for you to use STL in your extension.

Again, bear in mind that ABI incompatibilites may hinder you when using your extension in conjunction with other extensions or 3rd party libraries.

#### Strings

In the Defold engine, we use `const char*` instead of `std::string`. And writing your own dynamic array or hash table isn't very hard, but there are also good alternatives found online.



### Make functions hidden

Use the `static` keywork on functions local to your compile unit if possible. This lets the compiler do some optimizations, and
can both improve performance as well as reduce executable size.


# 3rd party libraries

When choosing a 3rd party library to use (regardless of language), we consider at least these things:

* Functionality - Does it solve the particular problem you have?
* Performance - Does it infer a performance cost in the runtime? For each frame, or
* Library size - How much bigger will the final executable be? Is it acceptable
* Dependencies - Does it require extra libraries
* Support - What state is the library in? Does it have many open issues? Is it still maintained? etc...
* License - Is it ok to use for this project?


# Open source dependencies

Always make sure that you have access to your dependencies.
E.g. if you depend on something on github, there's nothing preventing that repository either being removed, or suddenly changes
direction or ownership.

The code in that library will be injected into your game, so make sure the library does what it's supposed to do, and nothing more!

<legal note?>
