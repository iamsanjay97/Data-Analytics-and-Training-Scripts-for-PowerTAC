function C = offline(budget, K, n)

    cost = 0; % initial DR cost
    quantum = 1; % initial quantum

    % initial compensation array
    C = zeros(1, n);

    while(cost < budget)

        d = 1;
        largestIndex = 1;

        while(d <= n)

            if(Jump(K(d), C(d)) >= Jump(K(largestIndex), C(largestIndex)))

                largestIndex = d;
            end

            d = d + 1;
        end

        C(largestIndex) = C(largestIndex) + quantum;
        cost = cost + quantum;
    end

    function j = Jump(k, c)
        j = (1 - exp(-k*(c+1))) - (1 - exp(-k*c));
    end

end
