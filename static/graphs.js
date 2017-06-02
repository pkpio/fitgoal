angular.module('newYearGoalsApp', ['chart.js']);
angular.module('newYearGoalsApp').controller('MainController', function($scope) {
    // chart options
    $scope.options = {
        hover: {
            mode: "x-axis"
        },
        tooltips: {
            mode: "x-axis"
        },
        elements: {
            point: { 
                radius: 0
            }
        },
        scales: {
            xAxes: [{
                ticks: {
                    maxTicksLimit: 20
                }
            }]
        }
    };

    $scope.datasetOverride = [{
        lineTension: 0
    }]

    $scope.init = function(user_distances, user_target) {
        label_days = []
        target_dists = []
        actual_dists = []
        diff_dists = []
        for (var i = 0; i < user_distances.length; i++) {
            target = (i+1)*user_target/365;
            actual = user_distances[i];

            label_days.push("Day " + (i+1));
            target_dists.push(target.toFixed(1));
            actual_dists.push(actual.toFixed(1));
            diff_dists.push( (actual-target).toFixed(1) ) ;
        }

        // show data to scope
        $scope.labels = label_days;
        $scope.series = ['Distance covered', 'Target Distance'];
        $scope.data = [actual_dists,target_dists];

        $scope.diffLabels = label_days;
        $scope.diffSeries = ['Difference'];
        $scope.diffData = [diff_dists];
    }
});
