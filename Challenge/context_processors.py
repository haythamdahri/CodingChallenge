from Challenge.forms import SearchForm


def global_vars(request):
    search_form = SearchForm()
    context = {
        'search_form': search_form
    }
    return context