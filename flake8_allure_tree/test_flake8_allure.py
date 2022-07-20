from .flake8_allure import (
    ClassMissingAllureError,
    CLASS_DECORATOR_TREE,
    FlakeClassAllurePytestVisitor,
    FlakeMethodAllurePytestVisitor,
    MethodMissingAllureError,
    METHOD_DECORATOR_TREE,
    MyConfig,
)
from flake8_plugin_utils import assert_error, assert_not_error

config = MyConfig(
    class_tag_tree=CLASS_DECORATOR_TREE,
    method_tag_tree=METHOD_DECORATOR_TREE,
    test_class_name="Test*",
    test_method_name="test_*",
    strict_tree=False,
)


def test_required_decorators():
    assert_error(
        FlakeClassAllurePytestVisitor,
        """\
    @allure.story('')
    class Test1:
        def test():
            pass 
    """,
        ClassMissingAllureError,
        config=config,
        name="Test1",
        tree=CLASS_DECORATOR_TREE,
        deco="feature,label,tag",
    )


def test_no_required_decorators_without_allure():
    assert_not_error(
        FlakeClassAllurePytestVisitor,
        """\
    class Test1:
        def test():
            pass 
    """,
        config=config,
    )


def test_check_class_decorator_position():
    assert_not_error(
        FlakeClassAllurePytestVisitor,
        """\
    @allure.feature('')
    @allure.story('')
    @allure.label('')
    @allure.tag('')
    class Test1:
        def test():
            pass 
    """,
        config=config,
    )


def test_check_class_and_method_decorator_position():
    assert_error(
        FlakeClassAllurePytestVisitor,
        """\
    @allure.story('')
    class Test1:
        @allure.title()
        def test_1():
            pass 
    """,
        ClassMissingAllureError,
        config=config,
        name="Test1",
        tree=CLASS_DECORATOR_TREE,
        deco="feature,label,tag",
    )

    assert_error(
        FlakeMethodAllurePytestVisitor,
        """\
    @allure.story('')
    class Test1:
        @allure.title()
        def test_1():
            pass 
    """,
        MethodMissingAllureError,
        config=config,
        name="test_1",
        tree=METHOD_DECORATOR_TREE,
        deco="tag",
    )


def test_check_class_decorator_with_config():
    assert_error(
        FlakeClassAllurePytestVisitor,
        """\
    @allure.label('')
    class Test1:
        def test():
            pass 
    """,
        ClassMissingAllureError,
        config=MyConfig(
            class_tag_tree="story",
            method_tag_tree="title",
            test_class_name="Test*",
            test_method_name="test_*",
            strict_tree=False,
        ),
        name="Test1",
        tree="story",
        deco="story",
    )


def test_check_test_names_reges():
    assert_error(
        FlakeClassAllurePytestVisitor,
        """\
    @allure.story('')
    class FakeTestCaseSimple:
        def test123():
            pass 
    """,
        ClassMissingAllureError,
        config=MyConfig(
            class_tag_tree=CLASS_DECORATOR_TREE,
            method_tag_tree=METHOD_DECORATOR_TREE,
            test_class_name="*TestCase*",
            test_method_name="test_*",
            strict_tree=False,
        ),
        name="FakeTestCaseSimple",
        tree=CLASS_DECORATOR_TREE,
        deco="feature,label,tag",
    )


def test_check_test_names_reges_without():
    assert_not_error(
        FlakeClassAllurePytestVisitor,
        """\
    @allure.story('')
    class FakeTestCaseSimple:
        def test123():
            pass 
    """,
        config=MyConfig(
            class_tag_tree=CLASS_DECORATOR_TREE,
            method_tag_tree=METHOD_DECORATOR_TREE,
            test_class_name="TestCase*",
            test_method_name="test_*",
            strict_tree=False,
        ),
    )


def test_check_test_strict_tree():
    assert_error(
        FlakeClassAllurePytestVisitor,
        """\
    class Test1:
        def test_12():
            pass 
    """,
        ClassMissingAllureError,
        config=MyConfig(
            class_tag_tree=CLASS_DECORATOR_TREE,
            method_tag_tree=METHOD_DECORATOR_TREE,
            test_class_name="Test*",
            test_method_name="test_*",
            strict_tree=True,
        ),
        name="Test1",
        tree=CLASS_DECORATOR_TREE,
        deco="feature,story,label,tag",
    )
