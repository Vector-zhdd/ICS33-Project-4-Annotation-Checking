# Submitter: haodoz4(Zhang, Haodong)
# Partner  : yuxuez2(Zhou, Yuxue)
# We certify that we worked cooperatively on this programming
#   assignments, according to the rules for pair programming

from goody import type_as_str
import inspect

class Check_All_OK:
    """
    Check_All_OK class implements __check_annotation__ by checking whether each
      annotation passed to its constructor is OK; the first one that
      fails (by raising AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """
       
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_All_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        for annot in self._annotations:
            check(param, annot, value, check_history+'Check_All_OK check: '+str(annot)+' while trying: '+str(self)+'\n')


class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (by raising AssertionError) this classes raises AssertionError and prints
      its failure, along with a list of all annotations tried followed by the
      check_history.
    """
    
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_Any_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        failed = 0
        for annot in self._annotations: 
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param)+' failed annotation check(Check_Any_OK): value = '+repr(value)+\
                         '\n  tried '+str(self)+'\n'+check_history                 



class Check_Annotation:
    # First bind the class attribute to True allowing checking to occur (but
    #   only if the object's attribute self._checking_on is also bound to True)
    checking_on  = True
  
    # First bind self._checking_on = True, for checking the decorated function f
    def __init__(self, f):
        self._f = f
        self._checking_on = True

    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.  
    def check(self,param,annot,value,check_history=''):
        
        # Define local functions for checking, list/tuple, dict, set/frozenset,
        #   lambda/functions, and str (str for extra credit)
        # Many of these local functions called by check, call check on their
        #   elements (thus are indirectly recursive)

        # First compare check's function annotation with its arguments
        if annot == None:
            pass
        elif type(annot) is type:
            assert isinstance(value, annot), '\'{}\' failed annotation check(wrong type): value = \'{}\' \n\t\twas type {} ...should be type {}'.format(param, value, type(value).__name__, annot.__name__)
        elif type(annot) == list:
            assert isinstance(value, list), '\'{}\' failed annotation check(wrong type): value = \'{}\' \n\t\twas type {} ...should be type list'.format(param, value, type(value).__name__)
            if len(annot) == 1:
                if type(annot[0]) != list and type(annot[0]) != tuple:
                    for i in range(len(value)):
                        try:
                            self.check(param, annot[0], value[i], check_history)
                        except AssertionError as e:
                            check_history += '\nlist[{}] check: {}'.format(i, annot[0])
                            #assert False, '\'{}\' failed annotation check(wrong type): value = \'{}\' \n\t\twas type {} ...should be type {} {}'.format(param, value[i],                                                                                                                                                           #type(value[i]).__name__, annot[0].__name__, check_history)
                            assert False, '{} {}'.format(e, check_history)
                else:
                    for j in range(len(value)):
                        copy = check_history
                        check_history += '\nlist[{}] check: {}'.format(j, annot[0])
                        self.check(param, annot[0], value[j], check_history)
                        check_history = copy
                
            else:
                length_annot = len(annot)
                length_value = len(value)
                assert length_annot == length_value, '\'{}\' failed annotation check(wrong number of elements): value = {} \n\t\tannotation had {} elements {}'.format(param, value, length_annot, annot)
                for i in range(len(value)):
                    try:
                        self.check(param, annot[i], value[i])
                    except AssertionError:
                        check_history += 'list[{}] check: {}'.format(i, annot[i])
                        assert False, '\'{}\' failed annotation check(wrong type): value = \'{}\' \n\t\twas type {} ...should be type {} \n{}'.format(param, value[i], 
                                                                                                                                                      type(value[i]).__name__, annot[i].__name__, check_history)
        elif type(annot) == tuple:
            assert isinstance(value, tuple), '\'{}\' failed annotation check(wrong type): value = \'{}\' \n\t\twas type {} ...should be type tuple'.format(param, value, type(value).__name__)
            if len(annot) == 1:
                if type(annot[0]) != tuple and type(annot[0]) != list:
                    for i in range(len(value)):
                        try:
                            self.check(param, annot[0], value[i], check_history)
                        except AssertionError:
                            check_history += '\ntuple[{}] check: {}'.format(i, annot[0])
                            assert False, '\'{}\' failed annotation check(wrong type): value = \'{}\' \n\t\twas type {} ...should be type {} {}'.format(param, value[i], 
                                                                                                                                                          type(value[i]).__name__, annot[0].__name__, check_history)
                else:
                    for j in range(len(value)):
                        copy = check_history
                        check_history += '\ntuple[{}] check: {}'.format(j, annot[0])
                        self.check(param, annot[0], value[j], check_history)
                        check_history = copy
                 
            else:
                length_annot = len(annot)
                length_value = len(value)
                assert length_annot == length_value, '\'{}\' failed annotation check(wrong number of elements): value = {} \n\t\tannotation had {} elements {}'.format(param, value, length_annot, annot)
                for i in range(len(value)):
                    try:
                        self.check(param, annot[i], value[i])
                    except AssertionError:
                        check_history += 'tuple[{}] check: {}'.format(i, annot[i])
                        assert False, '\'{}\' failed annotation check(wrong type): value = \'{}\' \n\t\twas type {} ...should be type {} \n{}'.format(param, value[i], type(value[i]).__name__, annot[i].__name__, check_history)
                        
        elif type(annot) == dict: 
            assert isinstance(value, dict), '\'{}\' failed annotation check(wrong type): value = {} \n\t\twas type {} ...should be type dict'.format(param, value, type(value).__name__)
            assert len(annot) == 1, '\'{}\' annotation inconsistency: dict should have 1 item but had {} \n\t\tannotation = {}'.format(param, len(annot), annot)
            
            for k, v in value.items():
                if type(list(annot.values())[0]) == list or type(list(annot.values())[0]) == tuple or type(list(annot.values())[0]) == dict:
                    self.check(param, list(annot.values())[0], v, check_history)
                else:
                    # assert isinstance(k, list(annot.keys())[0]), '\'{}\' failed annotation check(wrong type): value = {} \n\twas type {} ...should be type {} \ndict key check: {}'.format(param, k, type(k).__name__, list(annot.keys())[0].__name__, list(annot.keys())[0])
                    # assert isinstance(v, list(annot.values())[0]), '\'{}\' failed annotation check(wrong type): value = {} \n\twas type {} ...should be type {} \ndict value check: {}'.format(param, v, type(v).__name__, list(annot.values())[0].__name__, list(annot.values())[0])
                    try:
                        self.check(param, list(annot.keys())[0], k, check_history)
                    except AssertionError:
                        assert False, '\'{}\' failed annotation check(wrong type): value = {} \n\twas type {} ...should be type {} \ndict key check: {}'.format(param, k, type(k).__name__, list(annot.keys())[0], list(annot.keys())[0])
                    try:
                        self.check(param, list(annot.values())[0], v, check_history)
                    except AssertionError:
                        assert False, '\'{}\' failed annotation check(wrong type): value = {} \n\twas type {} ...should be type {} \ndict value check: {}'.format(param, v, type(v).__name__, list(annot.values())[0], list(annot.values())[0])
                    




        elif type(annot) == set:
            assert isinstance(value, set), '\'{}\' failed annotation check(wrong type): value = \'{}\' \n\t\twas type {} ...should be type set'.format(param, value, type(value).__name__)
            length_annot = len(annot)
            assert length_annot <= 1, '\'{}\' annotation inconsistency: set should have 1 value but had {} \n\t\tannotation = {}'.format(param, length_annot, annot)
            for i in value:
                try:
                    self.check(param, list(annot)[0], i, check_history)
                except AssertionError:
                    check_history += '\nset value check: {}'.format(list(annot)[0])
                    assert False, '\'{}\' failed annotation check(wrong type): value = \'{}\' \n\t\twas type {} ...should be type {} {}'.format(param, i, 
                                                                                                                                                          type(i).__name__, list(annot)[0].__name__, check_history)
        elif type(annot) == frozenset:
            assert isinstance(value, frozenset), '\'{}\' failed annotation check(wrong type): value = \'{}\' \n\t\twas type {} ...should be type set'.format(param, value, type(value).__name__)
            length_annot = len(annot)
            assert length_annot <= 1, '\'{}\' annotation inconsistency: set should have 1 value but had {} \n\t\tannotation = {}'.format(param, length_annot, annot)
            for i in value:
                try:
                    self.check(param, list(annot)[0], i, check_history)
                except AssertionError:
                    check_history += '\nset value check: {}'.format(list(annot)[0])
                    assert False, '\'{}\' failed annotation check(wrong type): value = \'{}\' \n\t\twas type {} ...should be type {} {}'.format(param, i, 
                                                                                                                                                          type(i).__name__, list(annot)[0].__name__, check_history)
            
        elif inspect.isfunction(annot):
            length_value = len(inspect.signature(self._f).parameters)
            length_annot = len(inspect.signature(annot).parameters)
            assert length_value == length_annot, '\'{}\' annotation inconsistency: predicate should have {} parameter but had {} \n\t\tpredicate = {}'.format(param, length_value, length_annot, annot)
            try:
                assert annot(value)
            except AssertionError:
                assert False, '\'{}\' failed annotation check: value = {} \n\t\tpredicate = {} {}'.format(param, value, annot, check_history)
            except Exception as e:
                assert False, '\'{}\' annotation predicate({}) raised exception \n\t\texception = {} {}'.format(param, annot, repr(e), check_history)
                
        elif type(annot) == str:
            try:
                assert eval(annot, {param: self.argument_dict[param] for param in self.argument_dict})
            except AssertionError:
                assert False, '\'{}\' failed annotation check(str predicate: \'{}\') \n\targs for evaluation: {}'.format(param, annot, ' '.join(str(z) + '->' + str(self.argument_dict[z]) for z in self.argument_dict))
            except Exception as e:
                assert False, '\'{}\' annotation check (str predicate {}) raised exception \n\t\texception = {}'.format(param, annot, repr(e))
        else:
            try:
                annot.__check_annotation__(self.check,param,value,check_history)
            except AttributeError:
                assert False,'There is no __check_annotation__ method in the class'
            
                        
        
    # Return result of calling decorated function call, checking present
    #   parameter/return annotations if required
    def __call__(self, *args, **kargs):
        
        # Return the argument/parameter bindings as an OrderedDict (it's derived
        #   from a dict): bind the function header's parameters using its order
        def param_arg_bindings():
            f_signature  = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args,**kargs)
            for param in f_signature.parameters.values():
                if not (param.name in bound_f_signature.arguments):
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments

        # If annotation checking is turned off at the class or function level
        #   just return the result of calling the decorated function
        # Otherwise do all the annotation checking
        
        try:
            # For each detected annotation, check it using its parameter's value

            # Compute/remember the value of the decorated function
            
            # If 'return' is in the annotation, check it
            
            # Return the decorated answer
            
            if self._checking_on:
                self.argument_dict = param_arg_bindings()
                f_annotation = self._f.__annotations__
                for i in self.argument_dict:
                    if i in f_annotation:
                        self.check(i, f_annotation[i], self.argument_dict[i])
                result = self._f(*args, **kargs)
                if 'return' in f_annotation:
                    self.argument_dict['_return'] = result
                    self.check('_return', f_annotation['return'], result)
                return result
            else:
                return self._f(*args, **kargs)
            
        # On first AssertionError, print the source lines of the function and reraise 
        except AssertionError:
            # print(80*'-')
            # for l in inspect.getsourcelines(self._f)[0]: # ignore starting line #
            #     print(l.rstrip())
            # print(80*'-')
            raise




  
if __name__ == '__main__':     
    # an example of testing a simple annotation  
    # def f(x:int): pass
    # f = Check_Annotation(f)
    # f(3)
    # f('a')

    
    
   
    
    


    
    
    
           
    #driver tests
    import driver
    driver.default_file_name = 'bscp4F21.txt'
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
