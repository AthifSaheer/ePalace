// document.getElementById('ff').innerHTML = 'dffff'

$(document).ready(function(){
    $(".ajaxLoader").hide()
    $(".form-check-input").on('click', function(){
        var _filterObj = {};
        $(".form-check-input").each(function(index, ele){
            var _filterVal = $(this).val()
            var _filterKey = $(this).data('filter')
            _filterObj[_filterKey] = Array.from(document.querySelectorAll('input[data-filter='+_filterKey+']:checked')).map(function(){
                return ele.value;
            })
        })
        console.log(_filterObj)

        // Run ajax 
        $.ajax({
            url:'/filter-data',
            // method:'post',
            data:_filterObj,
            dataType:'json',
            beforeSend:function(){
                $(".ajaxLoader").html('Loading....')
            },
            success:function(res){
                $(".ajaxLoader").hide()
                console.log(res)
            }
        })
    })
})