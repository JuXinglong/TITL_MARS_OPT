import cplex


class MARS_OPT:

    def __init__(self):
        return

    def max_optimize(self, mars):
        X_UB = 1.0
        X_LB = -1.0
        M = 2.0
        isQuadratic = False
        opt_prob = cplex.Cplex()
        opt_prob.objective.set_sense(opt_prob.objective.sense.maximize)
        target = opt_prob.parameters.optimalitytarget.values
        opt_prob.parameters.optimalitytarget.set(target.optimal_global)
        n_var = 1 + mars.n_variables

        for i in range(mars.n_basis_fn):
            n_var += 2 * mars.basis_fns[i + 1].order
        dt = opt_prob.variables.type
        # data_types=[dt.continuous, dt.binary, dt.integer]
        data_types = [dt.continuous] + [dt.continuous] * mars.n_variables
        ub = [1] + [X_UB] * mars.n_variables
        lb = [1] + [X_LB] * mars.n_variables
        obj = [0] * n_var
        obj[0] = mars.coefficients[0, 0]

        var_index = 1 + mars.n_variables
        q_mat = [cplex.SparsePair(ind=[], val=[])] + [cplex.SparsePair(ind=[], val=[])] * mars.n_variables

        con_lin_expr = []
        con_senses = []
        con_rhs = []
        # self.knot_value = knot_value
        # self.index_of_variable = index_of_variable
        # self.sign = sign
        for i in range(mars.n_basis_fn):
            order = mars.basis_fns[i + 1].order
            if order == 1:
                obj[var_index] = mars.coefficients[i + 1, 0]
                data_types.extend([dt.continuous, dt.binary])
                ub.extend([M, 1])
                lb.extend([0, 0])
                q_mat.append(cplex.SparsePair(ind=[], val=[]))
                q_mat.append(cplex.SparsePair(ind=[], val=[]))
                # print(mars.basis_fns[i + 1].knot_items[0].knot_value)
                # print(mars.basis_fns[i + 1].knot_items[0].index_of_variable)
                # print(mars.basis_fns[i + 1].knot_items[0].sign)
                s = mars.basis_fns[i + 1].knot_items[0].sign
                k = mars.basis_fns[i + 1].knot_items[0].knot_value
                i_v = mars.basis_fns[i + 1].knot_items[0].index_of_variable + 1
                if s == 1:
                    con_lin_expr.extend([cplex.SparsePair(ind=[var_index, i_v], val=[1.0, -1.0]),
                                         cplex.SparsePair(ind=[var_index + 1, i_v, var_index], val=[-M, 1.0, -1.0]),
                                         cplex.SparsePair(ind=[var_index + 1, var_index], val=[M, -1.0])])
                    con_senses.extend(["G", "G", "G"])
                    con_rhs.extend([-k, k - M, 0])
                else:
                    con_lin_expr.extend([cplex.SparsePair(ind=[var_index, i_v], val=[1.0, 1.0]),
                                         cplex.SparsePair(ind=[var_index + 1, i_v, var_index], val=[-M, -1.0, -1.0]),
                                         cplex.SparsePair(ind=[var_index + 1, var_index], val=[M, -1.0])])
                    con_senses.extend(["G", "G", "G"])
                    con_rhs.extend([k, -M - k, 0])

                var_index += 2



            elif order == 2:
                isQuadratic = True
                q_mat.append(cplex.SparsePair(ind=[var_index + 2], val=[mars.coefficients[i + 1, 0]]))
                q_mat.append(cplex.SparsePair(ind=[], val=[]))

                s = mars.basis_fns[i + 1].knot_items[0].sign
                k = mars.basis_fns[i + 1].knot_items[0].knot_value
                i_v = mars.basis_fns[i + 1].knot_items[0].index_of_variable + 1
                if s == 1:
                    con_lin_expr.extend([cplex.SparsePair(ind=[var_index, i_v], val=[1.0, -1.0]),
                                         cplex.SparsePair(ind=[var_index + 1, i_v, var_index], val=[-M, 1.0, -1.0]),
                                         cplex.SparsePair(ind=[var_index + 1, var_index], val=[M, -1.0])])
                    con_senses.extend(["G", "G", "G"])
                    con_rhs.extend([-k, k - M, 0])
                else:
                    con_lin_expr.extend([cplex.SparsePair(ind=[var_index, i_v], val=[1.0, 1.0]),
                                         cplex.SparsePair(ind=[var_index + 1, i_v, var_index], val=[-M, -1.0, -1.0]),
                                         cplex.SparsePair(ind=[var_index + 1, var_index], val=[M, -1.0])])
                    con_senses.extend(["G", "G", "G"])
                    con_rhs.extend([k, -M - k, 0])

                var_index += 2
                q_mat.append(cplex.SparsePair(ind=[var_index - 2], val=[mars.coefficients[i + 1, 0]]))
                q_mat.append(cplex.SparsePair(ind=[], val=[]))

                s = mars.basis_fns[i + 1].knot_items[1].sign
                k = mars.basis_fns[i + 1].knot_items[1].knot_value
                i_v = mars.basis_fns[i + 1].knot_items[1].index_of_variable + 1
                if s == 1:
                    con_lin_expr.extend([cplex.SparsePair(ind=[var_index, i_v], val=[1.0, -1.0]),
                                         cplex.SparsePair(ind=[var_index + 1, i_v, var_index], val=[-M, 1.0, -1.0]),
                                         cplex.SparsePair(ind=[var_index + 1, var_index], val=[M, -1.0])])
                    con_senses.extend(["G", "G", "G"])
                    con_rhs.extend([-k, k - M, 0])
                else:
                    con_lin_expr.extend([cplex.SparsePair(ind=[var_index, i_v], val=[1.0, 1.0]),
                                         cplex.SparsePair(ind=[var_index + 1, i_v, var_index], val=[-M, -1.0, -1.0]),
                                         cplex.SparsePair(ind=[var_index + 1, var_index], val=[M, -1.0])])
                    con_senses.extend(["G", "G", "G"])
                    con_rhs.extend([k, -M - k, 0])

                var_index += 2
                data_types.extend([dt.continuous, dt.binary, dt.continuous, dt.binary])
                ub.extend([M, 1, M, 1])
                lb.extend([0, 0, 0, 0])
            else:
                print("problem!greater than 2 way interaction term!")
                return

        # print(con_lin_expr)
        # print(con_senses)
        # print(con_rhs)

        # opt_prob.linear_constraints.add(lin_expr=con_lin_expr, senses=con_senses, rhs=con_rhs)
        # print(obj)
        # print(data_types)
        # print(q_mat)
        opt_prob.variables.add(obj=obj, types=data_types, lb=lb, ub=ub)

        if isQuadratic:
            opt_prob.objective.set_quadratic(q_mat)
        opt_prob.linear_constraints.add(lin_expr=con_lin_expr, senses=con_senses, rhs=con_rhs)
        # print(var_index)
        # indices = c.linear_constraints.add(
        #     lin_expr=[cplex.SparsePair(ind=["x1", "x3"], val=[1.0, -1.0]),
        #               cplex.SparsePair(ind=["x1", "x2"], val=[1.0, 1.0]),
        #               cplex.SparsePair(ind=["x1", "x2", "x3"], val=[-1.0] * 3),
        #               cplex.SparsePair(ind=["x2", "x3"], val=[10.0, -2.0])],
        #     senses=["E", "L", "G", "R"],
        #     rhs=[0.0, 1.0, -1.0, 2.0],
        #     range_values=[0.0, 0.0, 0.0, -10.0],
        #     names=["c0", "c1", "c2", "c3"])

        # opt_prob.linear_constraints.add(lin_expr=[cplex.SparsePair(ind=[0, 3], val=[1.0, -1.0])],
        #                                           senses=["E"], rhs=[0.0])
        # print(obj)
        # print(mars.coefficients)
        opt_prob.write('mars.lp')
        opt_prob.solve()
        # opt_prob.solution.get_status()
        r = opt_prob.solution.get_objective_value()
        x = opt_prob.solution.get_values()
        print("R", r)
        print("x", [x[1:1 + mars.n_variables]])
        print("x_original", mars.X_inverse_scale([x[1:1 + mars.n_variables]]))
        print("predict", mars.predict(mars.X_inverse_scale([x[1:1 + mars.n_variables]])))
        # print(mars.basis_fns[5].order)
        # p = cplex.Cplex()
        # p.objective.set_sense(p.objective.sense.maximize)
        # obj = [1.0, 2.0]
        # ub = [2, 4]
        # lb = [-1, -2]
        # p.variables.add(obj=obj, ub=ub, lb=lb)
        #
        # target = p.parameters.optimalitytarget.values
        # p.parameters.optimalitytarget.set(target.optimal_global)
        opt_x = mars.X_inverse_scale([x[1:1 + mars.n_variables]])
        opt_x = opt_x[0]
        return opt_x.tolist() + [r]

    def min_optimize(self, mars):
        X_UB = 1.0
        X_LB = -1.0
        M = 2.0
        isQuadratic = False
        opt_prob = cplex.Cplex()
        opt_prob.objective.set_sense(opt_prob.objective.sense.minimize)
        target = opt_prob.parameters.optimalitytarget.values
        opt_prob.parameters.optimalitytarget.set(target.optimal_global)
        n_var = 1 + mars.n_variables

        for i in range(mars.n_basis_fn):
            n_var += 2 * mars.basis_fns[i + 1].order
        dt = opt_prob.variables.type
        # data_types=[dt.continuous, dt.binary, dt.integer]
        data_types = [dt.continuous] + [dt.continuous] * mars.n_variables
        ub = [1] + [X_UB] * mars.n_variables
        lb = [1] + [X_LB] * mars.n_variables
        obj = [0] * n_var
        obj[0] = mars.coefficients[0, 0]

        var_index = 1 + mars.n_variables
        q_mat = [cplex.SparsePair(ind=[], val=[])]+[cplex.SparsePair(ind=[], val=[])]*mars.n_variables

        con_lin_expr = []
        con_senses = []
        con_rhs = []
        # self.knot_value = knot_value
        # self.index_of_variable = index_of_variable
        # self.sign = sign
        for i in range(mars.n_basis_fn):
            order = mars.basis_fns[i + 1].order
            if order == 1:
                obj[var_index] = mars.coefficients[i + 1, 0]
                data_types.extend([dt.continuous, dt.binary])
                ub.extend([M, 1])
                lb.extend([0, 0])
                q_mat.append(cplex.SparsePair(ind=[], val=[]))
                q_mat.append(cplex.SparsePair(ind=[], val=[]))
                # print(mars.basis_fns[i + 1].knot_items[0].knot_value)
                # print(mars.basis_fns[i + 1].knot_items[0].index_of_variable)
                # print(mars.basis_fns[i + 1].knot_items[0].sign)
                s = mars.basis_fns[i + 1].knot_items[0].sign
                k = mars.basis_fns[i + 1].knot_items[0].knot_value
                i_v = mars.basis_fns[i + 1].knot_items[0].index_of_variable + 1
                if s == 1:
                    con_lin_expr.extend([cplex.SparsePair(ind=[var_index, i_v], val=[1.0, -1.0]),
                                         cplex.SparsePair(ind=[var_index + 1, i_v, var_index], val=[-M, 1.0, -1.0]),
                                         cplex.SparsePair(ind=[var_index + 1, var_index], val=[M, -1.0])])
                    con_senses.extend(["G", "G", "G"])
                    con_rhs.extend([-k, k - M, 0])
                else:
                    con_lin_expr.extend([cplex.SparsePair(ind=[var_index, i_v], val=[1.0, 1.0]),
                                         cplex.SparsePair(ind=[var_index + 1, i_v, var_index], val=[-M, -1.0, -1.0]),
                                         cplex.SparsePair(ind=[var_index + 1, var_index], val=[M, -1.0])])
                    con_senses.extend(["G", "G", "G"])
                    con_rhs.extend([k, -M - k, 0])

                var_index += 2



            elif order == 2:
                isQuadratic = True
                q_mat.append(cplex.SparsePair(ind=[var_index + 2], val=[mars.coefficients[i + 1, 0]]))
                q_mat.append(cplex.SparsePair(ind=[], val=[]))

                s = mars.basis_fns[i + 1].knot_items[0].sign
                k = mars.basis_fns[i + 1].knot_items[0].knot_value
                i_v = mars.basis_fns[i + 1].knot_items[0].index_of_variable + 1
                if s == 1:
                    con_lin_expr.extend([cplex.SparsePair(ind=[var_index, i_v], val=[1.0, -1.0]),
                                         cplex.SparsePair(ind=[var_index + 1, i_v, var_index], val=[-M, 1.0, -1.0]),
                                         cplex.SparsePair(ind=[var_index + 1, var_index], val=[M, -1.0])])
                    con_senses.extend(["G", "G", "G"])
                    con_rhs.extend([-k, k - M, 0])
                else:
                    con_lin_expr.extend([cplex.SparsePair(ind=[var_index, i_v], val=[1.0, 1.0]),
                                         cplex.SparsePair(ind=[var_index + 1, i_v, var_index], val=[-M, -1.0, -1.0]),
                                         cplex.SparsePair(ind=[var_index + 1, var_index], val=[M, -1.0])])
                    con_senses.extend(["G", "G", "G"])
                    con_rhs.extend([k, -M - k, 0])

                var_index += 2
                q_mat.append(cplex.SparsePair(ind=[var_index - 2], val=[mars.coefficients[i + 1, 0]]))
                q_mat.append(cplex.SparsePair(ind=[], val=[]))

                s = mars.basis_fns[i + 1].knot_items[1].sign
                k = mars.basis_fns[i + 1].knot_items[1].knot_value
                i_v = mars.basis_fns[i + 1].knot_items[1].index_of_variable + 1
                if s == 1:
                    con_lin_expr.extend([cplex.SparsePair(ind=[var_index, i_v], val=[1.0, -1.0]),
                                         cplex.SparsePair(ind=[var_index + 1, i_v, var_index], val=[-M, 1.0, -1.0]),
                                         cplex.SparsePair(ind=[var_index + 1, var_index], val=[M, -1.0])])
                    con_senses.extend(["G", "G", "G"])
                    con_rhs.extend([-k, k - M, 0])
                else:
                    con_lin_expr.extend([cplex.SparsePair(ind=[var_index, i_v], val=[1.0, 1.0]),
                                         cplex.SparsePair(ind=[var_index + 1, i_v, var_index], val=[-M, -1.0, -1.0]),
                                         cplex.SparsePair(ind=[var_index + 1, var_index], val=[M, -1.0])])
                    con_senses.extend(["G", "G", "G"])
                    con_rhs.extend([k, -M - k, 0])

                var_index += 2
                data_types.extend([dt.continuous, dt.binary, dt.continuous, dt.binary])
                ub.extend([M, 1, M, 1])
                lb.extend([0, 0, 0, 0])
            else:
                print("problem!greater than 2 way interaction term!")
                return

        # print(con_lin_expr)
        # print(con_senses)
        # print(con_rhs)

        # opt_prob.linear_constraints.add(lin_expr=con_lin_expr, senses=con_senses, rhs=con_rhs)
        # print(obj)
        # print(data_types)
        # print(q_mat)
        opt_prob.variables.add(obj=obj, types=data_types, lb=lb, ub=ub)

        if isQuadratic:
            opt_prob.objective.set_quadratic(q_mat)
        opt_prob.linear_constraints.add(lin_expr=con_lin_expr, senses=con_senses, rhs=con_rhs)
        # print(var_index)
        # indices = c.linear_constraints.add(
        #     lin_expr=[cplex.SparsePair(ind=["x1", "x3"], val=[1.0, -1.0]),
        #               cplex.SparsePair(ind=["x1", "x2"], val=[1.0, 1.0]),
        #               cplex.SparsePair(ind=["x1", "x2", "x3"], val=[-1.0] * 3),
        #               cplex.SparsePair(ind=["x2", "x3"], val=[10.0, -2.0])],
        #     senses=["E", "L", "G", "R"],
        #     rhs=[0.0, 1.0, -1.0, 2.0],
        #     range_values=[0.0, 0.0, 0.0, -10.0],
        #     names=["c0", "c1", "c2", "c3"])

        # opt_prob.linear_constraints.add(lin_expr=[cplex.SparsePair(ind=[0, 3], val=[1.0, -1.0])],
        #                                           senses=["E"], rhs=[0.0])
        # print(obj)
        # print(mars.coefficients)
        opt_prob.write('mars.lp')
        opt_prob.solve()
        # opt_prob.solution.get_status()
        r = opt_prob.solution.get_objective_value()
        x = opt_prob.solution.get_values()
        print("R", r)
        print("x", [x[1:1 + mars.n_variables]])
        print("x_original", mars.X_inverse_scale([x[1:1 + mars.n_variables]]))
        print("predict", mars.predict(mars.X_inverse_scale([x[1:1 + mars.n_variables]])))
        # print("predict", mars.predict(mars.X_inverse_scale([[0, 0]])))


        # print(mars.basis_fns[5].order)
        # p = cplex.Cplex()
        # p.objective.set_sense(p.objective.sense.maximize)
        # obj = [1.0, 2.0]
        # ub = [2, 4]
        # lb = [-1, -2]
        # p.variables.add(obj=obj, ub=ub, lb=lb)
        #
        # target = p.parameters.optimalitytarget.values
        # p.parameters.optimalitytarget.set(target.optimal_global)
        opt_x = mars.X_inverse_scale([x[1:1 + mars.n_variables]])
        opt_x = opt_x[0]
        return opt_x.tolist() + [r]



