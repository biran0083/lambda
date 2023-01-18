from lambda_expr import *
import sys
import unittest

class TestLambda(unittest.TestCase):

    def setUp(self):
        sys.setrecursionlimit(1000000)

    def test_boolean(self):
        self.assertTrue(natify_bool(eval_lambda_exp(true)))
        self.assertFalse(natify_bool(eval_lambda_exp(false)))

    def test_church_numeral(self):
        self.assertTrue(natify_bool(eval_lambda_exp(is_zero(church_numeral(0)))))
        self.assertFalse(natify_bool(eval_lambda_exp(is_zero(church_numeral(1)))))
        self.assertEqual(0, natify_church_numeral(eval_lambda_exp(church_numeral(0))))
        self.assertEqual(1, natify_church_numeral(eval_lambda_exp(church_numeral(1))))
        self.assertEqual(10, natify_church_numeral(eval_lambda_exp(church_numeral(10))))
        self.assertEqual(200, natify_church_numeral(eval_lambda_exp(church_numeral(200))))

    def test_add(self):
        exp = add(church_numeral(10), church_numeral(11))
        self.assertEqual(21, natify_church_numeral(eval_lambda_exp(exp)))

    def test_mul(self):
        exp = mul(church_numeral(10), church_numeral(11))
        self.assertEqual(110, natify_church_numeral(eval_lambda_exp(exp)))

    def test_sub(self):
        exp = sub(church_numeral(10), church_numeral(3))
        self.assertEqual(7, natify_church_numeral(eval_lambda_exp(exp)))

    def test_list(self):
        self.assertTrue(natify_bool(eval_lambda_exp(is_nil(nil))))
        lst = int_list([1])
        self.assertFalse(natify_bool(eval_lambda_exp(is_nil(lst))))
        self.assertTrue(natify_bool(eval_lambda_exp(is_pair(lst))))
        self.assertEqual(1, natify_church_numeral(eval_lambda_exp(first(lst))))
        self.assertTrue(natify_bool(eval_lambda_exp(is_nil(rest(lst)))))
        self.assertEqual([1], natify_int_list(eval_lambda_exp(lst)))

        lst = int_list([1,2,3])
        self.assertEqual([1,2,3], natify_int_list(eval_lambda_exp(lst)))

    def test_let(self):
        self.assertEqual(1, natify_church_numeral(eval_lambda_exp(let('a', church_numeral(1), 'a'))))
        self.assertEqual(3, natify_church_numeral(eval_lambda_exp(
            let('a', church_numeral(1), 
                let('b', church_numeral(2),
                    add('a', 'b'))))))

    def test_function(self):
        self.assertEqual(3, natify_church_numeral(eval_lambda_exp(let('inc', 
                                                                      function('x', 
                                                                               add('x', church_numeral(1))), 
                                                                      call('inc', church_numeral(2))))))

    def test_if_expr(self):
        self.assertTrue(natify_bool(eval_lambda_exp(
            if_expr(is_zero(church_numeral(0)),
                   true,
                   false))))
        self.assertFalse(natify_bool(eval_lambda_exp(
            if_expr(is_zero(church_numeral(1)),
                   true,
                   false))))
        self.assertEqual(1, natify_church_numeral(eval_lambda_exp(
            if_expr(is_zero(church_numeral(0)),
                   church_numeral(1),
                   church_numeral(2)))))
        self.assertEqual(2, natify_church_numeral(eval_lambda_exp(
            if_expr(is_zero(church_numeral(1)),
                   church_numeral(1),
                   church_numeral(2)))))
        

    def test_let_rec(self):
        self.assertEqual(3, natify_church_numeral(eval_lambda_exp(
            let_rec('inc', 
              function('x', 
                       add('x', church_numeral(1))), 
              call('inc', church_numeral(2))))))

    def test_fib(self):
        def fib(n):
            return let_rec('fib',
                           function('n',
                                    if_expr(less_than('n', church_numeral(2)),
                                            'n',
                                            add(call('fib', sub('n', church_numeral(1))),
                                                call('fib', sub('n', church_numeral(2)))))),
                           call('fib', n))
        self.assertEqual(0, natify_church_numeral(eval_lambda_exp(fib(church_numeral(0))))) 
        self.assertEqual(1, natify_church_numeral(eval_lambda_exp(fib(church_numeral(1))))) 
        self.assertEqual(1, natify_church_numeral(eval_lambda_exp(fib(church_numeral(2))))) 
        self.assertEqual(2, natify_church_numeral(eval_lambda_exp(fib(church_numeral(3))))) 
        self.assertEqual(3, natify_church_numeral(eval_lambda_exp(fib(church_numeral(4))))) 
        self.assertEqual(5, natify_church_numeral(eval_lambda_exp(fib(church_numeral(5))))) 

    def test_recursion(self):
        def fact(n):
            return let_rec('fact',
                           function('n',
                                    if_expr(is_zero('n'),
                                           church_numeral(1),
                                           mul('n', 
                                               call('fact', sub('n', church_numeral(1)))))),
                           call('fact', church_numeral(n)))

        self.assertEqual(1, natify_church_numeral(eval_lambda_exp(fact(0))))
        self.assertEqual(1, natify_church_numeral(eval_lambda_exp(fact(1))))
        self.assertEqual(2, natify_church_numeral(eval_lambda_exp(fact(2))))
        self.assertEqual(6, natify_church_numeral(eval_lambda_exp(fact(3))))
        self.assertEqual(24, natify_church_numeral(eval_lambda_exp(fact(4))))
        self.assertEqual(120, natify_church_numeral(eval_lambda_exp(fact(5))))

    def test_multi_arg_call(self):
        exp = multi_arg_call(multi_arg_function([], church_numeral(0)), [])
        self.assertEqual(0, natify_church_numeral(eval_lambda_exp(exp)))
        exp = multi_arg_call(multi_arg_function(['a'], 'a'), [church_numeral(1)])
        self.assertEqual(1, natify_church_numeral(eval_lambda_exp(exp)))
        exp = multi_arg_call(multi_arg_function(['a', 'b'], add('a', 'b')), [church_numeral(1), church_numeral(2)])
        self.assertEqual(3, natify_church_numeral(eval_lambda_exp(exp)))

    def test_reverse(self):
        def reverse(l):
            return let_rec('helper',
                           multi_arg_function(
                               ['l', 'res'],
                               if_expr(is_nil('l'),
                                       'res',
                                       multi_arg_call('helper',
                                                      [rest('l'), pair(first('l'), 'res')]))),
                           multi_arg_call('helper', [l, nil]))
        exp = reverse(int_list([]))
        self.assertEqual([], natify_int_list(eval_lambda_exp(exp)))
        exp = reverse(int_list([1]))
        self.assertEqual([1], natify_int_list(eval_lambda_exp(exp)))
        exp = reverse(int_list([1,2]))
        self.assertEqual([2,1], natify_int_list(eval_lambda_exp(exp)))
        exp = reverse(int_list([1,2,3]))
        self.assertEqual([3,2,1], natify_int_list(eval_lambda_exp(exp)))

    def test_list_append(self):
        def append(l1, l2):
            return let_rec('append',
                           multi_arg_function(
                               ['l1', 'l2'],
                                if_expr(is_nil('l1'),
                                       'l2',
                                       pair(first('l1'),
                                            multi_arg_call('append', 
                                                          [rest('l1'), 'l2'])))),
                           multi_arg_call('append', [l1, l2]))
        exp = append(int_list([1,2]), int_list([]))
        self.assertEqual([1, 2], natify_int_list(eval_lambda_exp(exp)))
        exp = append(int_list([1,2]), int_list([3, 4]))
        self.assertEqual([1, 2, 3, 4], natify_int_list(eval_lambda_exp(exp)))
        exp = append(int_list([]), int_list([3, 4]))
        self.assertEqual([3, 4], natify_int_list(eval_lambda_exp(exp)))

    def test_split(self):
        def split(l):
            return let_rec('split',
                           multi_arg_function(['l', 'l1', 'l2'],
                                              if_expr(is_nil('l'),
                                                            pair('l1', 'l2'),
                                                            multi_arg_call('split',
                                                                           [
                                                                               rest('l'),
                                                                               'l2',
                                                                               pair(first('l'), 'l1'),
                                                                               ]))),
                           multi_arg_call('split', [l, nil, nil]))
        exp = split(int_list([1,2,3,4]))
        self.assertEqual([3,1], natify_int_list(eval_lambda_exp(first(exp))))
        self.assertEqual([4,2], natify_int_list(eval_lambda_exp(rest(exp))))

    def test_less_than(self):
        self.assertTrue(natify_bool(eval_lambda_exp(less_than(church_numeral(1), church_numeral(2)))))
        self.assertFalse(natify_bool(eval_lambda_exp(less_than(church_numeral(2), church_numeral(2)))))
        self.assertFalse(natify_bool(eval_lambda_exp(less_than(church_numeral(3), church_numeral(2)))))

    def test_merge(self):
        def merge(l1, l2):
            return let_rec('merge',
                           multi_arg_function(['l1', 'l2'],
                                              if_expr(is_nil('l1'),
                                                      'l2',
                                                      if_expr(is_nil('l2'),
                                                              'l1',
                                                              if_expr(less_than(first('l1'), first('l2')),
                                                                      pair(first('l1'), multi_arg_call('merge', [rest('l1'), 'l2'])),
                                                                      pair(first('l2'), multi_arg_call('merge', ['l1', rest('l2')])))))),
                           multi_arg_call('merge', [l1, l2]))
        exp = merge(int_list([5]), int_list([1]))
        self.assertEqual([1, 5], natify_int_list(eval_lambda_exp(exp)))
        exp = merge(int_list([1,4]), int_list([2,3]))
        self.assertEqual([1,2,3,4], natify_int_list(eval_lambda_exp(exp)))

    def test_merge_sort(self):
        def msort(l):
            return let_rec('msort',
                           function('l',
                                    let_rec('split',
                                            multi_arg_function(['l', 'l1', 'l2'],
                                                               if_expr(is_nil('l'),
                                                                       pair('l1', 'l2'),
                                                                       multi_arg_call('split',
                                                                                      [
                                                                                          rest('l'),
                                                                                          'l2',
                                                                                          pair(first('l'), 'l1'),
                                                                                          ]))),
                                            let_rec('merge',
                                                    multi_arg_function(['l1', 'l2'],
                                                        if_expr(is_nil('l1'),
                                                                'l2',
                                                                if_expr(is_nil('l2'),
                                                                        'l1',
                                                                        if_expr(less_than(first('l1'), first('l2')),
                                                                                pair(first('l1'), multi_arg_call('merge', [rest('l1'), 'l2'])),
                                                                                pair(first('l2'), multi_arg_call('merge', ['l1', rest('l2')])))))),
                                                    if_expr(or_expr(is_nil('l'), is_nil(rest('l'))),
                                                            'l',
                                                            let('parts',
                                                                multi_arg_call('split', ['l', nil, nil]),
                                                                multi_arg_call('merge',
                                                                               [
                                                                                   call('msort', first('parts')),
                                                                                   call('msort', rest('parts')),
                                                                               ])))))),
                           call('msort', l))
        exp = msort(int_list([5]))
        self.assertEqual([5], natify_int_list(eval_lambda_exp(exp)))
        exp = msort(int_list([5,1]))
        self.assertEqual([1,5], natify_int_list(eval_lambda_exp(exp)))
        exp = msort(int_list([5,4,3,2,1]))
        self.assertEqual([1,2,3,4,5], natify_int_list(eval_lambda_exp(exp)))

if __name__ == '__main__':
    unittest.main()


