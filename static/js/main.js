$(function () {
    var datePicker = $('#interaction_reminder_time');
    var now = new Date(+new Date() + 10 * 60 * 1000);
    datePicker.datetimepicker({
        inline: true,
        sideBySide: true,
        minDate: now,
        icons: {
            time: 'fa fa-clock-o',
            date: 'fa fa-calendar',
            up: 'fa fa-chevron-up',
            down: 'fa fa-chevron-down',
            previous: 'fa fa-chevron-left',
            next: 'fa fa-chevron-right',
            today: 'fa fa-calendar-check-o',
            clear: 'fa fa-trash-o',
            close: 'fa fa-close'
        }
    });
});

 var delay = (function () {
            var timer = 0;
            return function (callback, ms) {
                clearTimeout(timer);
                timer = setTimeout(callback, ms);
            };
        })();

        var results = $("#results");

        var buildResults = function(data) {
            var rLink = "<a class='client-result'></a>";
            var rBox = "<div class='results-box'></div>";

            for (var key in data) {
                if (data.hasOwnProperty(key)) {
                    var found = false;
                    var resultContainer = $(rBox);
                    var resultType = key.charAt(0).toUpperCase() + key.slice(1);
                    resultContainer.html("<h2>" + resultType + "</h2>");
                    var resultData = data[key];
                    for (var i = 0; i < resultData.length; i++) {
                        found = true;
                        var resultLink = $(rLink);
                        resultLink.html(resultData[i].name);
                        resultLink.attr('href', '/client/' + resultData[i].pk);
                        resultContainer.append(resultLink);
                    } if (!found) {
                        resultContainer.append("Sorry, there were no " + resultType + "found.");
                    }
                    results.append(resultContainer);
                }
            }
        };

        var search = $("#search");

        var performSearch = function(searchTerm) {
            $.get( "/api/search/" + searchTerm, function( data ) {
                buildResults(data);
            }).fail( function() {
                results.html("Problem with request");
            });
        };
        $(document).ready(function(){
            if (search.val()) {
                performSearch(search.val());
            }
        });
        search.on("keyup", function() {
            var searchTerm = $(this).val();
            if (searchTerm) {
                delay(function() {
                    results.empty();
                    performSearch(searchTerm);
                }, 500)
            } else {
                results.empty();
            }
        });