# Resume Reader

Resume Reader is a simple app that uses a file as input and processes it with regular expressions to extract sections' data.

There are 3 main files:

* ***server.py*** - defines the GET request logic for /resume endpoint. It also adds Swagger information and descriptions.
* ***cli.py*** - defines the logic for CLI command to retrieve information from the input file.
* ***utils.py*** - contains the commonly used functions of extracting, parsing and structuring the information.

## Commands

### Running JSON Rest API

> cd src
>
> python server.py
>
> Go to http://127.0.0.1:5000/ and make requests with or without section parameter

### Running Flask CLI

> cd src
>
> python server.py
>
> flask resume read [section], where section can be All/About/Contact/Education/Experience/Skills/Projects/Languages.