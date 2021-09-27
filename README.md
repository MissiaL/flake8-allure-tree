# flake8-allure-tree

Plugin for checking the order of allure tags

You can set tag tree by options:

```
--class-tag-tree=feature>story>label>tag
--method-tag-tree=title>tag
--test-class-name=Test*
--test-method-name=test_*
--strict-tree=False
```

Use `--strict-tree` options if you want your tests to be strictly allure tagged.
By default, tests are checked that contain at least one allure decorator.

Install:

`pip install -e git+https://github.com/missial/flake8-allure-tree#egg=flake8-allure-tree`