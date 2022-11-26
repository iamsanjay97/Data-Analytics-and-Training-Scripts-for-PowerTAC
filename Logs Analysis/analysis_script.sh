##### All Availible options of Classes to analyse #####

server_path="/mnt/d/PowerTAC/PowerTAC2021/server/server-distribution/log"

# specify the names of boot-files to analyze
declare -a boot_files=( "powertac-sim-finals_2019_07_6_498" )
for boot in ${boot_files[@]}

do
    echo "Analysing $boot"
    output_path="/mnt/d/PowerTAC/PowerTAC2022/experiments/logtool_results/tariff_RL_strategy_v1_0/three_player_test2/$boot"
    mkdir $output_path

    mvn exec:exec -Dexec.args="org.powertac.logtool.example.BrokerAccounting $server_path/$boot.state $output_path/BrokerAccounting.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.BrokerBalancingActions $server_path/$boot.state $output_path/BrokerBalancingActions.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.BrokerCosts $server_path/$boot.state $output_path/BrokerCosts.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.BrokerImbalanceCost $server_path/$boot.state $output_path/BrokerImbalanceCost.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.BrokerMktPrices $server_path/$boot.state $output_path/BrokerMktPrices.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.BrokerPriceAnomaly $server_path/$boot.state $output_path/BrokerPriceAnomaly.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.CapacityAnalysis $server_path/$boot.state $output_path/CapacityAnalysis.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.CapacityValidator $server_path/$boot.state $output_path/CapacityValidator.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.CustomerBalancingCapacity $server_path/$boot.state $output_path/CustomerBalancingCapacity.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.CustomerProductionConsumption $server_path/$boot.state $output_path/CustomerProductionConsumption.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.CustomerStats $server_path/$boot.state $output_path/CustomerStats.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.DemandResponseStats $server_path/$boot.state $output_path/DemandResponseStats.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.EnergyMixStats $server_path/$boot.state $output_path/EnergyMixStats.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.GameBrokerInfo $server_path/$boot.state $output_path/GameBrokerInfo.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.ImbalanceCostAnalysis $server_path/$boot.state $output_path/ImbalanceCostAnalysis.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.ImbalanceStats $server_path/$boot.state $output_path/ImbalanceStats.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.ImbalanceSummary $server_path/$boot.state $output_path/ImbalanceSummary.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.MeritOrder $server_path/$boot.state $output_path/MeritOrder.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.MktPriceStats $server_path/$boot.state $output_path/MktPriceStats.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.ProductionConsumption $server_path/$boot.state $output_path/ProductionConsumption.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.ProductionConsumptionWeather $server_path/$boot.state $output_path/ProductionConsumptionWeather.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.SolarProduction $server_path/$boot.state $output_path/SolarProduction.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.TariffAnalysis $server_path/$boot.state $output_path/TariffAnalysis.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.TariffMktShare $server_path/$boot.state $output_path/TariffMktShare.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.TotalDemand $server_path/$boot.state $output_path/TotalDemand.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.WeatherForecastStats $server_path/$boot.state $output_path/WeatherForecastStats.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.WeatherStats $server_path/$boot.state $output_path/WeatherStats.csv"
    mvn exec:exec -Dexec.args="org.powertac.logtool.example.WindStats $server_path/$boot.state $output_path/WindStats.csv"
done

