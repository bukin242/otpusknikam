$(function() {

    q = $('input[name="q"]')

    if(q.length)
    {
        val = q.val();

        if(!val)
        {
            $('input[name="q"]').focus();

        }

    }

});
