
<!DOCTYPE html>
<html>
<head>
    <title>View Comments</title>
</head>
<body>  
    <h1>View your Comments!</h1>
    <form action="/view_comments/{{ glitz_id }}" method="POST">    
        Chosen grid area: {{select_grid_name}}
        <br>
        <select name="select_grids" onchange="this.form.submit()">
            {% for grid in grids %}
                <option value="{{ grid.grid_id }}"
                        {% if grid.grid_id == select_grid_id %} 
                            selected="selected"
                        {% endif %}>
                    {{ grid.grid_name }}
                </option>
            {% endfor %}
        </select>
    </form>

    <table>
       {% for comment in comments %}
        <tr>
            <td>
                {{ comment.comment_text }}         
            </td>
        </tr>
        {% endfor %}
    </table>

</br></br>

<footer>© Copyright Glitzy</footer>



</body>
</html>
</html>
