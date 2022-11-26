function [K_estimate, regret_heur, best_red, cur_red] = online(budget, n, K_actual, batch, number_of_rounds)    

    K_estimate          = 0.01.*ones(1,n);
    K_estimate_plus     = K_estimate;
    probabilities       = zeros(1, n); 
    number_of_discounts = budget;
        
    offered_hist = zeros(n, number_of_discounts+1);
    success_hist = zeros(n, number_of_discounts+1);
    
    t = 0;
    cur_red = 0.0;
    best_red = 0.0;
    regret_heur             = zeros(1,number_of_rounds/batch);
   
    C_actual = offline(budget, K_actual, n); 
  
    while(t < number_of_rounds)
        
        C_estimates         = offline(budget, K_estimate_plus, n);
        
        for j = 1:n
            probabilities(j) = 1 - exp(-K_actual(j)*C_estimates(j));
        end      

        offered_inst        = zeros(n, number_of_discounts+1);
        success_inst        = zeros(n, number_of_discounts+1);
        
        for j = 1:n
            if C_estimates(j) ~= 0
                offered_inst(j, C_estimates(j)) = offered_inst(j, C_estimates(j)) + batch;
                success_inst(j, C_estimates(j)) = success_inst(j, C_estimates(j)) + binornd(batch, probabilities(j));%(C_estimates(j), probabilities(j));
            end
        end
        
        for j = 1:n
            if C_estimates(j) ~= 0
                offered_hist(j, C_estimates(j)) = offered_hist(j, C_estimates(j)) + offered_inst(j, C_estimates(j));
                success_hist(j, C_estimates(j)) = success_hist(j, C_estimates(j)) + success_inst(j, C_estimates(j));
            end
        end      
        t = t + batch;
        [K_estimate, K_estimate_plus] = estimate_lamda_ls(success_hist, offered_hist, n, number_of_discounts, t);
       
        for j = 1:n
            best_red = best_red + batch * (1 - exp(-K_actual(j) * C_actual(j)));
        end
        
        cur_red = cur_red + sum(success_inst, 'all');
      
        regret_heur(t/batch) = (best_red - cur_red);   
    end
end

% Functions %

function [lamda_estimate, lamda_plus] = estimate_lamda_ls(succ_hist, off_hist, n, number_of_discounts,t)
	prob            = ones(1, number_of_discounts);  % shouldn't be zeros
    lamda_estimate	= ones(1,n);
    lamda_plus      = ones(1,n);
       
	for i=1:n
        lambda_max = 0;
        lambda_min = 5.0;
        lamda_estimate_i=.6*ones(1,number_of_discounts);
        for j=1:number_of_discounts
            if off_hist(i,j) ~=0
				prob(j)             = succ_hist(i,j)/off_hist(i,j);
				lamda_estimate_i(j) = max(0.00000001, -log(1-prob(j)+0.00000001)/j);
            
                if lamda_estimate_i(j) > lambda_max
                    lambda_max = lamda_estimate_i(j);
                end

                if lamda_estimate_i(j) < lambda_min
                    lambda_min = lamda_estimate_i(j);
                end
            end
        end
      
		err = 500000000.0; 
        
        if((t == 100) || (t == 1000) || (t == 10000) || (t == 100000) || (t == 1000000) || (t == 5000000))
            
            k_list = [];
            err_list = [];
            
            % prob
            for k=0.01:0.00005:1.0
                temp_err = 0.0;
                for j=1: number_of_discounts
                    temp_err = temp_err + ((prob(j) - (1-exp(-k*j))))*((prob(j) - (1-exp(-k*j))));
                end
                
                k_list = [k_list, k];
                err_list = [err_list, temp_err];
                
                if temp_err < err
                    err = temp_err;
                    lamda_estimate(i) = k;
                end
            end
            
            % lamda_estimate
            % hold on;
            % plot(k_list, err_list);
            
        else		
            for k=lambda_min:0.00005:lambda_max
                temp_err = 0.0;
                for j=1: number_of_discounts
                    temp_err = temp_err + ((prob(j) - (1-exp(-k*j))))*((prob(j) - (1-exp(-k*j))));
                end
                if temp_err < err
                    err = temp_err;
                    lamda_estimate(i) = k;
                end
            end
        end
        
        offered_i = sum(off_hist(i,:));
		lamda_plus(i) = lamda_estimate(i) + sqrt(2*log(t)/(offered_i));
	end
end
