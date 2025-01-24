from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Deck
from .forms import DeckForm
from card.models import Card


# Create your views here.
class DeckList(generic.ListView):
    """
    displays all public decks
    """
    queryset = Deck.objects.filter(published=1)
    template_name = "deckbuilder/deck_list.html"
    paginate_by = 12

class MyDecks(generic.ListView):
    """
    displays all of user's decks
    """
    template_name = "deckbuilder/my_decks.html"
    paginate_by = 12

    def get_queryset(self):
        return Deck.objects.filter(author=self.request.user)
    

def deck_detail(request, id):
    """
    Display an individual :model:`deckbuilder.Deck`

    **Context**

    ``deck``
        An instance of :model:`deckbuilder.Deck`.

    **Template:**

    :template:`deckbuilder/deck_detail.html`
    """
    queryset = Deck.objects.all()
    deck = get_object_or_404(queryset, id=id)
    card_ids = deck.deck_content.split(',')
    deck_cards = Card.objects.filter(card_id__in=card_ids)

    return render(
        request,
        "deckbuilder/deck_detail.html",
        {
            "deck": deck,
            "deck_cards": deck_cards
        },
    )


def deckbuilder(request):
    """
    Builds a deck as :model:`deckbuilder.Deck`.
    Displays cards to choose from :model:`card.Card`.

    **Context**
    ``deck_form``
        An instance of :form:`deckbuilder.DeckForm`

    ``cards``
        An instance of :model:`card.Card`.

    **Template:**

    :template:`deckbuilder/deckbuilder.html`
    """
    cards = Card.objects.all()
    deck_form = DeckForm()

    if request.method == "POST":
        deck_form = DeckForm(data=request.POST)
        if deck_form.is_valid():
            saved_deck = deck_form.save(commit=False)
            saved_deck.author = request.user
            saved_deck.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Deck saved successfully'
            )
            return HttpResponseRedirect(reverse('deck_detail', args=[saved_deck.id]))
        else:
            messages.add_message(
                request, messages.ERROR,
                'Error while saving deck.'
            )

    return render(
        request,
        "deckbuilder/deckbuilder.html",
        {
            "cards": cards,
            "deck_form": deck_form
        },
    )