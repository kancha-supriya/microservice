# RAML
## What is RAML?
[RAML](http://raml.org/) is a structured language (based off of YAML) for describing an API.  Using it we can describe:

- Routes
- Parameters
- Example responses
- Header, query parameter, and post body validation schemas.
- [And much more ...](https://github.com/raml-org/raml-spec/blob/master/versions/raml-08/raml-08.md)

## Why use RAML?

When we have several developers working on a microservice, RAML can help us agree on the API contract before development even begins. Doing this, we also unblock the consumer application (generally frontend code, but possibly another microservice) from waiting until the microservice is complete.

- It's a structured language instead of markdown or other open document format
- It's machine parse-able (more on that below)
- It acts as a contract between developers

## How can I write RAML?

Although it is a structured language, YAML is pretty forgiving and truthfully, we are not linting or compiling RAML in any way. This can lead to some messiness but we have some tools we can use.

#### [API Designer](https://github.com/mulesoft/api-designer)
API Designer can be installed via node, runs on your localhost:3000. It provides a nice "IDE" for programming your RAML with helpful syntax warnings and errors as well as a sidebar that lets you graphically explore your API.

```bash
npm install -g api-designer
api-designer
```

![Screenshot of RAML API Designer](https://c1.staticflickr.com/9/8762/28685564721_b6e60eb7f0_c.jpg)

#### [API Workbench](http://apiworkbench.com/docs/)
It is for the Atom editor. It provides very similar functionality to API Designer, but inside Atom.
