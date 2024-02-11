# coding-challenge-1-wc
Coding Challenge 1: Build Your Own WC Tool  

## Usage:

### Make ccwc visible to the current shell

```
CCWC_DIR="path_to_dir_containing_ccwc"
source $CCWC_DIR/init
```

### Get a list of available options
`ccwc -h`

### Count the number of bytes in a file:
`ccwc -c path_to_file`

### Count the number of lines in a file:
`ccwc -l path_to_file`

### Count the number of words in a file:
`ccwc -w path_to_file`