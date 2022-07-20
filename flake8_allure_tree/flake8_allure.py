import ast
import fnmatch

from flake8.options.manager import OptionManager
from flake8_plugin_utils import Plugin, Visitor, Error

__version__ = "0.1.0"

CLASS_DECORATOR_TREE = "feature>story>label>tag"
METHOD_DECORATOR_TREE = "title>tag"


class ClassMissingAllureError(Error):
    code = "AL001"
    message = "Class '{name}' should have tags the right position: {tree}. Required '{deco}' decorators"  # noqa: E501


class MethodMissingAllureError(Error):
    code = "AL002"
    message = "Method '{name}' should have tags the right position: {tree}. Required '{deco}' decorators"  # noqa: E501


def _matches_prefix_or_glob_option(pattern: str, name: str) -> bool:
    if name.startswith(pattern):
        return True
    elif ("*" in pattern or "?" in pattern or "[" in pattern) and fnmatch.fnmatch(
        name, pattern
    ):
        return True
    return False


def _get_required_decorators(node, decorators, strict_tree):
    if not decorators:
        return
    decorators_tree = decorators.split(">")

    allure_decorators = [
        d
        for d in node.decorator_list
        if isinstance(d, ast.Call)
        and getattr(getattr(d.func, "value", None), "id", None) == "allure"
    ]

    if not allure_decorators and not strict_tree:
        return

    for decorator in allure_decorators:
        allure_method = decorator.func.attr
        if allure_method not in decorators_tree:
            continue
        index = decorators_tree.index(allure_method)
        decorators_tree.pop(index)

    return decorators_tree


class Config:
    def __init__(
        self,
        class_tag_tree,
        method_tag_tree,
        test_class_name,
        test_method_name,
        strict_tree,
    ):
        self.class_tag_tree = class_tag_tree
        self.method_tag_tree = method_tag_tree
        self.test_class_name = test_class_name
        self.test_method_name = test_method_name
        self.strict_tree = strict_tree


class FlakeClassAllurePytestVisitor(Visitor):
    def _is_test_class(self, node):
        name = getattr(node, "name", None)
        if name:
            class_pattern = self.config.test_class_name
            return _matches_prefix_or_glob_option(class_pattern, name)

    def visit_ClassDef(self, node) -> None:
        if self._is_test_class(node):
            required_decorators = _get_required_decorators(
                node, self.config.class_tag_tree, self.config.strict_tree
            )
            if required_decorators:
                self.error_from_node(
                    ClassMissingAllureError,
                    node,
                    name=node.name,
                    tree=self.config.class_tag_tree,
                    deco=",".join(required_decorators),
                )


class FlakeMethodAllurePytestVisitor(Visitor):
    def _is_test_method(self, node):
        name = getattr(node, "name", None)
        if name:
            test_pattern = self.config.test_method_name
            return _matches_prefix_or_glob_option(test_pattern, name)

    def visit_ClassDef(self, node) -> None:
        for method in node.body:
            if self._is_test_method(method):
                required_decorators = _get_required_decorators(
                    method, self.config.method_tag_tree, self.config.strict_tree
                )
                if required_decorators:
                    self.error_from_node(
                        MethodMissingAllureError,
                        method,
                        name=method.name,
                        tree=self.config.method_tag_tree,
                        deco=",".join(required_decorators),
                    )


class AllurePytestPlugin(Plugin):
    name = "flake8_allure_tree"
    version = __version__
    visitors = [FlakeClassAllurePytestVisitor, FlakeMethodAllurePytestVisitor]

    @classmethod
    def add_options(cls, options_manager: OptionManager):
        options_manager.add_option(
            "--class-tag-tree",
            default=CLASS_DECORATOR_TREE,
            parse_from_config=True,
        )
        options_manager.add_option(
            "--method-tag-tree",
            default=METHOD_DECORATOR_TREE,
            parse_from_config=True,
        )
        options_manager.add_option(
            "--test-class-name",
            default="Test*",
            help="Support glob pattern",
            parse_from_config=True,
        )
        options_manager.add_option(
            "--test-method-name",
            default="test_*",
            help="Support glob pattern",
            parse_from_config=True,
        )
        options_manager.add_option(
            "--strict-tree",
            action="store_true",
            help="Use strict tree. Unconditionally checks for tags in all tests",
            parse_from_config=True,
        )

    @classmethod
    def parse_options_to_config(cls, option_manager, options, args):
        return Config(
            class_tag_tree=options.class_tag_tree,
            method_tag_tree=options.method_tag_tree,
            test_class_name=options.test_class_name,
            test_method_name=options.test_method_name,
            strict_tree=options.strict_tree,
        )
