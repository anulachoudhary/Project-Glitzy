function GetWishes(_page) {
 
    var _offset = (_page - 1) * 2;
   
    $.ajax({
        url: '/getWish',
        type: 'POST',
        data: {
            offset: _offset
        },
        success: function(res) {
 
            var itemsPerPage = 2;
 
            var wishObj = JSON.parse(res);
 
            $('#ulist').empty();
            $('#listTemplate').tmpl(wishObj[0]).appendTo('#ulist');
 
            var total = wishObj[1]['total'];
            var pageCount = total / itemsPerPage;
            var pageRem = total % itemsPerPage;
            if (pageRem != 0) {
                pageCount = Math.floor(pageCount) + 1;
            }
 
 
            $('.pagination').empty();
 
            var pageStart = $('#hdnStart').val();
            var pageEnd = $('#hdnEnd').val();
 
 
 
 
            if (pageStart > 5) {
                var aPrev = $('<a/>').attr({
                        'href': '#'
                    }, {
                        'aria-label': 'Previous'
                    })
                    .append($('<span/>').attr('aria-hidden', 'true').html('&laquo;'));
 
                $(aPrev).click(function() {
                    $('#hdnStart').val(Number(pageStart) - 5);
                    $('#hdnEnd').val(Number(pageStart) - 5 + 4);
                    GetWishes(Number(pageStart) - 5);
                });
 
                var prevLink = $('<li/>').append(aPrev);
                $('.pagination').append(prevLink);
            }
 
 
 
            for (var i = Number(pageStart); i <= Number(pageEnd); i++) {
 
                if (i > pageCount) {
                    break;
                }
 
 
                var aPage = $('<a/>').attr('href', '#').text(i);
 
                $(aPage).click(function(i) {
                    return function() {
                        GetWishes(i);
                    }
                }(i));
                var page = $('<li/>').append(aPage);
 
                if ((_page) == i) {
                    $(page).attr('class', 'active');
                }
 
                $('.pagination').append(page);
 
 
            }
            if ((Number(pageStart) + 5) <= pageCount) {
                var nextLink = $('<li/>').append($('<a/>').attr({
                        'href': '#'
                    }, {
                        'aria-label': 'Next'
                    })
                    .append($('<span/>').attr('aria-hidden', 'true').html('&raquo;').click(function() {
                        $('#hdnStart').val(Number(pageStart) + 5);
                        $('#hdnEnd').val(Number(pageStart) + 5 + 4);
                        GetWishes(Number(pageStart) + 5);
 
                    })));
                $('.pagination').append(nextLink);
            }
 
 
 
 
        },
        error: function(error) {
            console.log(error);
        }
    });
}