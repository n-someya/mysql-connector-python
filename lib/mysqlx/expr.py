# MySQL Connector/Python - MySQL driver written in Python.
# Copyright (c) 2017, Oracle and/or its affiliates. All rights reserved.

# MySQL Connector/Python is licensed under the terms of the GPLv2
# <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>, like most
# MySQL Connectors. There are special exceptions to the terms and
# conditions of the GPLv2 as it is applied to this software, see the
# FOSS License Exception
# <http://www.mysql.com/about/legal/licensing/foss-exception.html>.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

from .compat import STRING_TYPES, PY3
from .protobuf import Message, mysqlxpb_enum


if PY3:
    xrange = range


class TokenType:
    NOT = 1
    AND = 2
    OR = 3
    XOR = 4
    IS = 5
    LPAREN = 6
    RPAREN = 7
    LSQBRACKET = 8
    RSQBRACKET = 9
    BETWEEN = 10
    TRUE = 11
    NULL = 12
    FALSE = 13
    IN = 14
    LIKE = 15
    INTERVAL = 16
    REGEXP = 17
    ESCAPE = 18
    IDENT = 19
    LSTRING = 20
    LNUM = 21
    DOT = 22
    DOLLAR = 23
    COMMA = 24
    EQ = 25
    NE = 26
    GT = 27
    GE = 28
    LT = 29
    LE = 30
    BITAND = 31
    BITOR = 32
    BITXOR = 33
    LSHIFT = 34
    RSHIFT = 35
    PLUS = 36
    MINUS = 37
    MUL = 38
    DIV = 39
    HEX = 40
    BIN = 41
    NEG = 42
    BANG = 43
    MICROSECOND = 44
    SECOND = 45
    MINUTE = 46
    HOUR = 47
    DAY = 48
    WEEK = 49
    MONTH = 50
    QUARTER = 51
    YEAR = 52
    EROTEME = 53
    DOUBLESTAR = 54
    MOD = 55
    COLON = 56
    OROR = 57
    ANDAND = 58
    LCURLY = 59
    RCURLY = 60
    CAST = 61
    DOTSTAR = 62
    ORDERBY_ASC = 63
    ORDERBY_DESC = 64
    AS = 65

interval_units = set([
    TokenType.MICROSECOND,
    TokenType.SECOND,
    TokenType.MINUTE,
    TokenType.HOUR,
    TokenType.DAY,
    TokenType.WEEK,
    TokenType.MONTH,
    TokenType.QUARTER,
    TokenType.YEAR])

# map of reserved word to token type
reservedWords = {
    "and":      TokenType.AND,
    "or":       TokenType.OR,
    "xor":      TokenType.XOR,
    "is":       TokenType.IS,
    "not":      TokenType.NOT,
    "like":     TokenType.LIKE,
    "in":       TokenType.IN,
    "regexp":   TokenType.REGEXP,
    "between":  TokenType.BETWEEN,
    "interval": TokenType.INTERVAL,
    "escape":   TokenType.ESCAPE,
    "cast":     TokenType.CAST,
    "div":      TokenType.DIV,
    "hex":      TokenType.HEX,
    "bin":      TokenType.BIN,
    "true":     TokenType.TRUE,
    "false":    TokenType.FALSE,
    "null":     TokenType.NULL,
    "second":   TokenType.SECOND,
    "minute":   TokenType.MINUTE,
    "hour":     TokenType.HOUR,
    "day":      TokenType.DAY,
    "week":     TokenType.WEEK,
    "month":    TokenType.MONTH,
    "quarter":  TokenType.QUARTER,
    "year":     TokenType.YEAR,
    "microsecond": TokenType.MICROSECOND,
    "asc":      TokenType.ORDERBY_ASC,
    "desc":     TokenType.ORDERBY_DESC,
    "as":       TokenType.AS
}


class Token:
    def __init__(self, type, val, len=1):
        self.type = type
        self.val = val
        self.len = len

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self.type == TokenType.IDENT or self.type == TokenType.LNUM or \
           self.type == TokenType.LSTRING:
            return str(self.type) + "(" + self.val + ")"
        else:
            return str(self.type)


# static protobuf helper functions

def build_null_scalar():
    msg = Message("Mysqlx.Datatypes.Scalar")
    msg["type"] = mysqlxpb_enum("Mysqlx.Datatypes.Scalar.Type.V_NULL")
    return msg


def build_double_scalar(d):
    msg = Message("Mysqlx.Datatypes.Scalar")
    msg["type"] = mysqlxpb_enum("Mysqlx.Datatypes.Scalar.Type.V_DOUBLE")
    msg["v_double"] = d
    return msg


def build_int_scalar(i):
    msg = Message("Mysqlx.Datatypes.Scalar")
    msg["type"] = mysqlxpb_enum("Mysqlx.Datatypes.Scalar.Type.V_SINT")
    msg["v_signed_int"] = i
    return msg


def build_string_scalar(s):
    if isinstance(s, STRING_TYPES):
        s = bytes(bytearray(s, "utf-8"))
    msg = Message("Mysqlx.Datatypes.Scalar")
    msg["type"] = mysqlxpb_enum("Mysqlx.Datatypes.Scalar.Type.V_STRING")
    msg["v_string"] = Message("Mysqlx.Datatypes.Scalar.String", value=s)
    return msg


def build_bool_scalar(b):
    msg = Message("Mysqlx.Datatypes.Scalar")
    msg["type"] = mysqlxpb_enum("Mysqlx.Datatypes.Scalar.Type.V_BOOL")
    msg["v_bool"] = b
    return msg


def build_literal_expr(anyval):
    msg = Message("Mysqlx.Expr.Expr")
    msg["type"] = mysqlxpb_enum("Mysqlx.Expr.Expr.Type.LITERAL")
    msg["literal"] = anyval
    return msg


def build_unary_op(name, param):
    operator = Message("Mysqlx.Expr.Expr")
    operator["name"] = name
    operator["param"] = [param]
    msg = Message("Mysqlx.Datatypes.Scalar")
    msg["type"] = mysqlxpb_enum("Mysqlx.Expr.Expr.Type.OPERATOR")
    msg["operator"] = operator.get_message()
    return msg


def escape_literal(string):
    return string.replace('"', '""')


class ExprParser:
    def __init__(self, string, allowRelational):
        self.string = string
        self.tokens = []
        self.pos = 0
        self._allowRelationalColumns = allowRelational
        self.placeholder_name_to_position = {}
        self.positional_placeholder_count = 0
        self.lex()

    # convencience checker for lexer
    def next_char_is(self, i, c):
        return i + 1 < len(self.string) and self.string[i + 1] == c

    def lex_number(self, pos):
        # numeric literal
        start = pos
        found_dot = False
        while pos < len(self.string) and (self.string[pos].isdigit() or
                                          self.string[pos] == "."):
            if self.string[pos] == ".":
                if found_dot is True:
                    raise ValueError("Invalid number. Found multiple '.'")
                found_dot = True
            # technically we allow more than one "." and let float()'s parsing
            # complain later
            pos = pos + 1
        val = self.string[start:pos]
        t = Token(TokenType.LNUM, val, len(val))
        return t

    def lex_alpha(self, i):
        start = i
        while i < len(self.string) and (self.string[i].isalnum() or
                                        self.string[i] == "_"):
            i = i + 1
        val = self.string[start:i]
        try:
            token = Token(reservedWords[val.lower()], val.upper(), len(val))
        except KeyError:
            token = Token(TokenType.IDENT, val, len(val))
        return token

    def lex_quoted_token(self, i):
        quote_char = self.string[i]
        val = ""
        i += 1
        start = i
        while i < len(self.string):
            c = self.string[i]
            if c == quote_char and i + 1 < len(self.string) and \
               self.string[i + 1] != quote_char:
                # break if we have a quote char that's not double
                break
            elif c == quote_char or c == "\\":
                # this quote char has to be doubled
                if i + 1 >= len(self.string):
                    break
                i += 1
                val += self.string[i]
            else:
                val += c
            i += 1
        if i >= len(self.string) or self.string[i] != quote_char:
            raise ValueError("Unterminated quoted string starting at {0}"
                             "".format(start))
        if quote_char == "`":
            return Token(TokenType.IDENT, val, len(val) + 2)
        else:
            return Token(TokenType.LSTRING, val, len(val) + 2)

    def lex(self):
        i = 0
        while i < len(self.string):
            c = self.string[i]
            if c.isspace():
                i += 1
                continue
            elif c.isdigit():
                token = self.lex_number(i)
            elif c.isalpha() or c == "_":
                token = self.lex_alpha(i)
            elif c == "?":
                token = Token(TokenType.EROTEME, c)
            elif c == ":":
                token = Token(TokenType.COLON, c)
            elif c == "{":
                token = Token(TokenType.LCURLY, c)
            elif c == "}":
                token = Token(TokenType.RCURLY, c)
            elif c == "+":
                token = Token(TokenType.PLUS, c)
            elif c == "-":
                Token(TokenType.MINUS, c)
            elif c == "*":
                if self.next_char_is(i, "*"):
                    token = Token(TokenType.DOUBLESTAR, "**")
                else:
                    token = Token(TokenType.MUL, c)
            elif c == "/":
                token = Token(TokenType.DIV, c)
            elif c == "$":
                token = Token(TokenType.DOLLAR, c)
            elif c == "%":
                token = Token(TokenType.MOD, c)
            elif c == "=":
                if self.next_char_is(i, "="):
                    token = Token(TokenType.EQ, "==", 2)
                else:
                    token = Token(TokenType.EQ, "==", 1)
            elif c == "&":
                if self.next_char_is(i, "&"):
                    token = Token(TokenType.ANDAND, c)
                else:
                    token = Token(TokenType.BITAND, c)
            elif c == "|":
                if self.next_char_is(i, "|"):
                    token = Token(TokenType.OROR, "||")
                else:
                    token = Token(TokenType.BITOR, c)
            elif c == "(":
                token = Token(TokenType.LPAREN, c)
            elif c == ")":
                token = Token(TokenType.RPAREN, c)
            elif c == "[":
                token = Token(TokenType.LSQBRACKET, c)
            elif c == "]":
                token = Token(TokenType.RSQBRACKET, c)
            elif c == "~":
                token = Token(TokenType.NEG, c)
            elif c == ",":
                token = Token(TokenType.COMMA, c)
            elif c == "!":
                if self.next_char_is(i, "="):
                    token = Token(TokenType.NE, "!=")
                else:
                    token = Token(TokenType.BANG, c)
            elif c == "<":
                if self.next_char_is(i, "<"):
                    token = Token(TokenType.LSHIFT, "<<")
                elif self.next_char_is(i, "="):
                    token = Token(TokenType.LE, "<=")
                else:
                    token = Token(TokenType.LT, c)
            elif c == ">":
                if self.next_char_is(i, ">"):
                    token = Token(TokenType.RSHIFT, ">>")
                elif self.next_char_is(i, "="):
                    token = Token(TokenType.GE, ">=")
                else:
                    token = Token(TokenType.GT, c)
            elif c == ".":
                if self.next_char_is(i, "*"):
                    token = Token(TokenType.DOTSTAR, ".*")
                elif i + 1 < len(self.string) and self.string[i + 1].isdigit():
                    token = self.lex_number(i)
                else:
                    token = Token(TokenType.DOT, c)
            elif c == '"' or c == "'" or c == "`":
                token = self.lex_quoted_token(i)
            else:
                raise ValueError("Unknown character at {0}".format(i))
            self.tokens.append(token)
            i += token.len

    def assert_cur_token(self, type):
        if self.pos >= len(self.tokens):
            raise ValueError("Expected token type {0} at pos {1} but no "
                             "tokens left".format(type, self.pos))
        if self.tokens[self.pos].type != type:
            raise ValueError("Expected token type {0} at pos {1} but found "
                             "type {2}".format(type, self.pos,
                                               self.tokens[self.pos]))

    def cur_token_type_is(self, type):
        return self.pos_token_type_is(self.pos, type)

    def next_token_type_is(self, type):
        return self.pos_token_type_is(self.pos + 1, type)

    def pos_token_type_is(self, pos, type):
        return pos < len(self.tokens) and self.tokens[pos].type == type

    def consume_token(self, type):
        self.assert_cur_token(type)
        v = self.tokens[self.pos].val
        self.pos = self.pos + 1
        return v

    def paren_expr_list(self):
        """Parse a paren-bounded expression list for function arguments or IN
        list and return a list of Expr objects.
        """
        exprs = []
        self.consume_token(TokenType.LPAREN)
        if not self.cur_token_type_is(TokenType.RPAREN):
            exprs.append(self.expr())
            while self.cur_token_type_is(TokenType.COMMA):
                self.pos = self.pos + 1
                exprs.append(self.expr())
        self.consume_token(TokenType.RPAREN)
        return exprs

    def identifier(self):
        self.assert_cur_token(TokenType.IDENT)
        ident = Message("Mysqlx.Expr.Identifier")
        if self.next_token_type_is(TokenType.DOT):
            ident["schema_name"] = self.consume_token(TokenType.IDENT)
            self.consume_token(TokenType.DOT)
        ident["name"] = self.tokens[self.pos].val
        self.pos += 1
        return ident

    def function_call(self):
        function_call = Message("Mysqlx.Expr.Expr.function_call")
        function_call["name"] = self.identifier()
        function_call["param"] = [self.paren_expr_list()]
        msg_expr = Message("Mysqlx.Expr.Expr")
        msg_expr["type"] = mysqlxpb_enum("Mysqlx.Expr.Expr.Type.FUNC_CALL")
        msg_expr["function_call"] = function_call.get_message()
        return msg_expr

    def docpath_member(self):
        self.consume_token(TokenType.DOT)
        token = self.tokens[self.pos]

        if token.type == TokenType.IDENT:
            if token.val.startswith('`') and token.val.endswith('`'):
                raise ValueError("{0} is not a valid JSON/ECMAScript "
                                 "identifier".format(token.value))
            self.consume_token(TokenType.IDENT)
            member_name = token.val
        elif self.token.type == TokenType.LSTRING:
            self.consume_token(TokenType.LSTRING)
            member_name = token.val
        else:
            raise ValueError("Expected token type IDENT or LSTRING in JSON "
                             "path at token pos {0}".format(self.pos))
        doc_path_item = Message("Mysqlx.Expr.DocumentPathItem")
        doc_path_item["type"] = mysqlxpb_enum(
            "Mysqlx.Expr.DocumentPathItem.Type.MEMBER")
        doc_path_item["value"] = member_name
        return doc_path_item

    def docpath_array_loc(self):
        self.consume_token(TokenType.LSQBRACKET)
        if self.cur_token_type_is(TokenType.MUL):
            self.consume_token(TokenType.RSQBRACKET)
            doc_path_item = Message("Mysqlx.Expr.DocumentPathItem")
            doc_path_item["type"] = mysqlxpb_enum(
                "Mysqlx.Expr.DocumentPathItem.Type.ARRAY_INDEX_ASTERISK")
            return doc_path_item
        elif self.cur_token_type_is(TokenType.LNUM):
            v = int(self.consume_token(TokenType.LNUM))
            if v < 0:
                raise IndexError("Array index cannot be negative at {0}"
                                 "".format(self.pos))
            self.consume_token(TokenType.RSQBRACKET)
            doc_path_item = Message("Mysqlx.Expr.DocumentPathItem")
            doc_path_item["type"] = mysqlxpb_enum(
                "Mysqlx.Expr.DocumentPathItem.Type.ARRAY_INDEX")
            doc_path_item["index"] = v
            return doc_path_item
        else:
            raise ValueError("Exception token type MUL or LNUM in JSON "
                             "path array index at token pos {0}"
                             "".format(self.pos))

    def document_field(self):
        col_id = Message("Mysqlx.Expr.ColumnIdentifier")
        if self.cur_token_type_is(TokenType.IDENT):
            doc_path_item = Message("Mysqlx.Expr.DocumentPathItem")
            doc_path_item["type"] = mysqlxpb_enum(
                "Mysqlx.Expr.DocumentPathItem.Type.MEMBER")
            doc_path_item["value"] = self.consume_token(TokenType.IDENT)
            col_id["document_path"].extend([doc_path_item.get_message()])
        col_id["document_path"].extend(self.document_path())
        expr = Message("Mysqlx.Expr.Expr")
        expr["type"] = mysqlxpb_enum("Mysqlx.Expr.Expr.Type.IDENT")
        expr["identifier"] = col_id
        return expr

    def document_path(self):
        """Parse a JSON-style document path, like WL#7909, but prefix by @.
        instead of $. We parse this as a string because the protocol doesn't
        support it. (yet)
        """
        doc_path = []
        while True:
            if self.cur_token_type_is(TokenType.DOT):
                doc_path.append(self.docpath_member().get_message())
            elif self.cur_token_type_is(TokenType.DOTSTAR):
                self.consume_token(TokenType.DOTSTAR)
                doc_path_item = Message("Mysqlx.Expr.DocumentPathItem")
                doc_path_item["type"] = mysqlxpb_enum(
                    "Mysqlx.Expr.DocumentPathItem.Type.MEMBER_ASTERISK")
                doc_path.append(doc_path_item.get_message())
            elif self.cur_token_type_is(TokenType.LSQBRACKET):
                doc_path.append(self.docpath_array_loc().get_message())
            elif self.cur_token_type_is(TokenType.DOUBLESTAR):
                self.consume_token(TokenType.DOUBLESTAR)
                doc_path_item = Message("Mysqlx.Expr.DocumentPathItem")
                doc_path_item["type"] = mysqlxpb_enum(
                    "Mysqlx.Expr.DocumentPathItem.Type.DOUBLE_ASTERISK")
                doc_path.append(doc_path_item.get_message())
            else:
                break
        items = len(doc_path)
        if items > 0 and doc_path[items - 1]["type"] == \
           mysqlxpb_enum("Mysqlx.Expr.DocumentPathItem.Type.DOUBLE_ASTERISK"):
            raise ValueError("JSON path may not end in '**' at {0}"
                             "".format(self.pos))
        return doc_path

    def column_identifier(self):
        parts = []
        parts.append(self.consume_token(TokenType.IDENT))
        while self.cur_token_type_is(TokenType.DOT):
            self.consume_token(TokenType.DOT)
            parts.append(self.consume_token(TokenType.IDENT))
        if len(parts) > 3:
            raise ValueError("Too many parts to identifier at {0}"
                             "".format(self.pos))
        parts.reverse()
        col_id = Message("Mysqlx.Expr.ColumnIdentifier")
        # clever way to apply them to the struct
        for i in xrange(0, len(parts)):
            if i == 0:
                col_id["name"] = parts[0]
            elif i == 1:
                col_id["table_name"] = parts[1]
            elif i == 2:
                col_id["schema_name"] = parts[2]
        if self.cur_token_type_is(TokenType.DOLLAR):
            self.consume_token(TokenType.DOLLAR)
            col_id["document_path"] = self.document_path()

        msg_expr = Message("Mysqlx.Expr.Expr")
        msg_expr["type"] = mysqlxpb_enum("Mysqlx.Expr.Expr.Type.IDENT")
        msg_expr["identifier"] = col_id
        return msg_expr

    def next_token(self):
        if (self.pos >= len(self.tokens)):
            raise ValueError("Unexpected end of token stream")
        t = self.tokens[self.pos]
        self.pos += 1
        return t

    def expect_token(self, token_type):
        t = self.next_token()
        if t.type != token_type:
            raise ValueError("Expected token type {0}".format(token_type))

    def parse_json_doc(self):
        o = Object()

    def parse_place_holder(self, token):
        place_holder_name = ""
        if self.cur_token_type_is(TokenType.LNUM):
            place_holder_name = self.consume_token(TokenType.LNUM_INT)
        elif self.cur_token_type_is(TokenType.IDENT):
            place_holder_name = self.consume_token(TokenType.IDENT)
        elif token.type == TokenType.EROTEME:
            place_holder_name = str(self.positional_placeholder_count)
        else:
            raise ValueError("Invalid placeholder name at token pos {0}"
                             "".format(self.pos))

        place_holder_name = place_holder_name.lower()
        msg_expr = Message("Mysqlx.Expr.Expr")
        msg_expr["type"] = mysqlxpb_enum("Mysqlx.Expr.Expr.Type.PLACEHOLDER")
        if place_holder_name in self.placeholder_name_to_position:
            msg_expr["position"] = \
                self.placeholder_name_to_position[place_holder_name]
        else:
            msg_expr["position"] = self.positional_placeholder_count
            self.placeholder_name_to_position[place_holder_name] = \
                self.positional_placeholder_count
            self.positional_placeholder_count += 1
        return msg_expr

    def atomic_expr(self):
        """Parse an atomic expression and return a protobuf Expr object"""
        token = self.next_token()

        if token.type in [TokenType.EROTEME, TokenType.COLON]:
            return self.parse_place_holder(token)
        elif token.type == TokenType.LCURLY:
            return self.parse_json_doc()
        elif token.type == TokenType.CAST:
            # TODO implement pass
            pass
        elif token.type == TokenType.LPAREN:
            e = self.expr()
            self.expect_token(TokenType.RPAREN)
            return e
        elif token.type in [TokenType.PLUS, TokenType.MINUS]:
            pass
        elif token.type in [TokenType.PLUS, TokenType.MINUS]:
            peek = self.peek_token()
            if peek.type == TokenType.LNUM:
                self.tokens[self.pos].val = token.val + peek.val
                return self.atomic_expr()
            return build_unary_op(token.val, self.atomic_expr())
        elif token.type in [TokenType.NOT, TokenType.NEG, TokenType.BANG]:
            return build_unary_op(token.val, self.atomic_expr())
        elif token.type == TokenType.LSTRING:
            return build_literal_expr(build_string_scalar(token.val))
        elif token.type == TokenType.NULL:
            return build_literal_expr(build_null_scalar())
        elif token.type == TokenType.LNUM:
            if "." in token.val:
                return build_literal_expr(
                    build_double_scalar(float(token.val)))
            else:
                return build_literal_expr(build_int_scalar(int(token.val)))
        elif token.type in [TokenType.TRUE, TokenType.FALSE]:
            return build_literal_expr(
                build_bool_scalar(token.type == TokenType.TRUE))
        elif token.type == TokenType.DOLLAR:
            return self.document_field()
        elif token.type == TokenType.MUL:
            return self.starOperator()
        elif token.type == TokenType.IDENT:
            self.pos = self.pos - 1  # stay on the identifier
            if self.next_token_type_is(TokenType.LPAREN) or \
               (self.next_token_type_is(TokenType.DOT) and
               self.pos_token_type_is(self.pos + 2, TokenType.IDENT) and
               self.pos_token_type_is(self.pos + 3, TokenType.LPAREN)):
                # Function call
                return self.function_call()
            else:
                return (self.document_field()
                        if not self._allowRelationalColumns
                        else self.column_identifier())

#        if t.type == TokenType.EROTEME:
#            return build_literal_expr(build_string_scalar("?"))
#        elif t.type == TokenType.INTERVAL:
#            e = Expr()
#            e.type = Expr.OPERATOR
#            e.operator.name = "INTERVAL"
#            e.operator.param.add().CopyFrom(self.expr())
#            # validate the interval units
#            if self.pos < len(self.tokens) and self.tokens[self.pos].type in interval_units:
#                pass
#            else:
#                raise StandardError("Expected interval units at " + str(self.pos))
#            e.operator.param.add().CopyFrom(build_literal_expr(build_string_scalar(self.tokens[self.pos].val)))
#            self.pos = self.pos + 1
#            return e
        raise ValueError("Unknown token type = {0}  when expecting atomic "
                         "expression at {1}".format(token.type, self.pos))

    def parse_left_assoc_binary_op_expr(self, types, inner_parser):
        """Given a `set' of types and an Expr-returning inner parser function,
        parse a left associate binary operator expression"""
        lhs = inner_parser()
        while (self.pos < len(self.tokens) and
               self.tokens[self.pos].type in types):
            msg = Message("Mysqlx.Expr.Expr")
            msg["type"] = mysqlxpb_enum("Mysqlx.Expr.Expr.Type.OPERATOR")
            operator = Message("Mysqlx.Expr.Operator")
            operator["name"] = self.tokens[self.pos].val
            operator["param"] = [lhs.get_message()]
            self.pos += 1
            operator["param"].append(inner_parser().get_message())
            msg["operator"] = operator
            lhs = msg
        return lhs

    # operator precedence is implemented here
    def mul_div_expr(self):
        return self.parse_left_assoc_binary_op_expr(
            set([TokenType.MUL, TokenType.DIV, TokenType.MOD]),
            self.atomic_expr)

    def add_sub_expr(self):
        return self.parse_left_assoc_binary_op_expr(
            set([TokenType.PLUS, TokenType.MINUS]), self.mul_div_expr)

    def shift_expr(self):
        return self.parse_left_assoc_binary_op_expr(
            set([TokenType.LSHIFT, TokenType.RSHIFT]), self.add_sub_expr)

    def bit_expr(self):
        return self.parse_left_assoc_binary_op_expr(
            set([TokenType.BITAND, TokenType.BITOR, TokenType.BITXOR]),
            self.shift_expr)

    def comp_expr(self):
        return self.parse_left_assoc_binary_op_expr(
            set([TokenType.GE, TokenType.GT, TokenType.LE, TokenType.LT,
                 TokenType.EQ, TokenType.NE]), self.bit_expr)

    def ilri_expr(self):
        lhs = self.comp_expr()
        is_not = False
        if self.cur_token_type_is(TokenType.NOT):
            is_not = True
            self.consume_token(TokenType.NOT)
        if self.pos < len(self.tokens):
            params = [lhs]
            op_name = self.tokens[self.pos].val
            if self.cur_token_type_is(TokenType.IS):
                self.consume_token(TokenType.IS)
                # for IS, NOT comes AFTER
                if self.cur_token_type_is(TokenType.NOT):
                    is_not = True
                    self.consume_token(TokenType.NOT)
                params.append(self.comp_expr())
            elif self.cur_token_type_is(TokenType.IN):
                self.consume_token(TokenType.IN)
                params.extend(self.paren_expr_list())
            elif self.cur_token_type_is(TokenType.LIKE):
                self.consume_token(TokenType.LIKE)
                params.append(self.comp_expr())
                if self.cur_token_type_is(TokenType.ESCAPE):
                    self.consume_token(TokenType.ESCAPE)
                    params.append(self.comp_expr())
            elif self.cur_token_type_is(TokenType.BETWEEN):
                self.consume_token(TokenType.BETWEEN)
                params.append(self.comp_expr())
                self.consume_token(TokenType.AND)
                params.append(self.comp_expr())
            elif self.cur_token_type_is(TokenType.REGEXP):
                self.consume_token(TokenType.REGEXP)
                params.append(self.comp_expr())
            else:
                if is_not:
                    raise ValueError("Unknown token after NOT as pos {0}"
                                     "".format(self.pos))
                op_name = None  # not an operator we're interested in
            if op_name:
                operator = Message("Mysqlx.Expr.Operator")
                operator["name"] = op_name
                operator["param"] = [params]
                msg_expr = Message("Mysqlx.Expr.Expr")
                msg_expr["type"] = mysqlxpb_enum(
                    "Mysqlx.Expr.Expr.Type.OPERATOR")
                msg_expr["operator"] = operator.get_message()
                if is_not:
                    # wrap if `NOT'-prefixed
                    msg_expr = build_unary_op("NOT", msg_expr.get_message())
                lhs = msg_expr
        return lhs

    def and_expr(self):
        return self.parse_left_assoc_binary_op_expr(
            set([TokenType.AND, TokenType.ANDAND]), self.ilri_expr)

    def or_expr(self):
        return self.parse_left_assoc_binary_op_expr(
            set([TokenType.OR, TokenType.OROR]), self.and_expr)

    def expr(self):
        return self.or_expr()

    def parse_table_insert_field(self):
        return Message("Mysqlx.Crud.Column",
                       name=self.consume_token(TokenType.IDENT))

    def parse_table_update_field(self):
        return self.column_identifier().identifier

    def parse_table_select_projection(self):
        project_expr = []
        first = True
        while self.pos < len(self.tokens):
            if not first:
                self.consume_token(TokenType.COMMA)
            first = False
            projection = Message("Mysqlx.Crud.Projection", source=self.expr())
            if self.cur_token_type_is(TokenType.AS):
                self.consume_token(TokenType.AS)
                projection["alias"] = self.consume_token(TokenType.IDENT)
            else:
                self.pos -= 1
                projection["alias"] = self.consume_token(TokenType.IDENT)
            project_expr.append(projection.get_message())
        return project_expr

    def parse_order_spec(self):
        order_specs = []
        first = True
        while self.pos < len(self.tokens):
            if not first:
                self.consume_token(TokenType.COMMA)
            first = False
            order = Message("Mysqlx.Crud.Order", expr=self.expr())
            if self.cur_token_type_is(TokenType.ORDERBY_ASC):
                order["direction"] = mysqlxpb_enum(
                    "Mysqlx.Crud.Order.Direction.ASC")
                self.consume_token(TokenType.ORDERBY_ASC)
            elif self.cur_token_type_is(TokenType.ORDERBY_DESC):
                order["direction"] = mysqlxpb_enum(
                    "Mysqlx.Crud.Order.Direction.DESC")
                self.consume_token(TokenType.ORDERBY_DESC)
            order_specs.append(order.get_message())
        return order_specs

    def parse_expr_list(self):
        expr_list = []
        first = True
        while self.pos < len(self.tokens):
            if not first:
                self.consume_token(TokenType.COMMA)
            first = False
            expr_list.append(self.expr().get_message())
        return expr_list


def parseAndPrintExpr(expr_string, allowRelational=True):
    print(">>>>>>> parsing:  {0}".format(expr_string))
    p = ExprParser(expr_string, allowRelational)
    print(p.tokens)
    e = p.expr()
    print(e)


def x_test():
    parseAndPrintExpr("name like :name")
    return
    parseAndPrintExpr("10+1")
    parseAndPrintExpr("(abc == 1)")
    parseAndPrintExpr("(func(abc)=1)")
    parseAndPrintExpr("(abc = \"jess\")")
    parseAndPrintExpr("(abc = \"with \\\"\")")
    parseAndPrintExpr("(abc != .10)")
    parseAndPrintExpr("(abc != \"xyz\")")
    parseAndPrintExpr("a + b * c + d")
    parseAndPrintExpr("(a + b) * c + d")
    parseAndPrintExpr("(field not in ('a',func('b', 2.0),'c'))")
    parseAndPrintExpr("jess.age between 30 and death")
    parseAndPrintExpr("a + b * c + d")
    parseAndPrintExpr("x > 10 and Y >= -20")
    parseAndPrintExpr("a is true and b is null and C + 1 > 40 and "
                      "(time = now() or hungry())")
    parseAndPrintExpr("a + b + -c > 2")
    parseAndPrintExpr("now () + b + c > 2")
    parseAndPrintExpr("now () + @b + c > 2")
    parseAndPrintExpr("now () - interval +2 day > some_other_time() or "
                      "something_else IS NOT NULL")
    parseAndPrintExpr("\"two quotes to one\"\"\"")
    parseAndPrintExpr("'two quotes to one'''")
    parseAndPrintExpr("'different quote \"'")
    parseAndPrintExpr("\"different quote '\"")
    parseAndPrintExpr("`ident`")
    parseAndPrintExpr("`ident```")
    parseAndPrintExpr("`ident\"'`")
    parseAndPrintExpr("now () - interval -2 day")
    parseAndPrintExpr("? > x and func(?, ?, ?)")
    parseAndPrintExpr("a > now() + interval (2 + x) MiNuTe")
    parseAndPrintExpr("a between 1 and 2")
    parseAndPrintExpr("a not between 1 and 2")
    parseAndPrintExpr("a in (1,2,a.b(3),4,5,x)")
    parseAndPrintExpr("a not in (1,2,3,4,5,@x)")
    parseAndPrintExpr("a like b escape c")
    parseAndPrintExpr("a not like b escape c")
    parseAndPrintExpr("(1 + 3) in (3, 4, 5)")
    parseAndPrintExpr("`a crazy \"function\"``'name'`(1 + 3) in (3, 4, 5)")
    parseAndPrintExpr("`a crazy \"function\"``'name'`(1 + 3) in (3, 4, 5)")
    parseAndPrintExpr("a@.b", False)
    parseAndPrintExpr("a@.b[0][0].c**.d.\"a weird\\\"key name\"", False)
    parseAndPrintExpr("a@.*", False)
    parseAndPrintExpr("a@[0].*", False)
    parseAndPrintExpr("a@**[0].*", False)

# x_test()