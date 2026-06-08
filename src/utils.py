def accordion_hidden_from(hide: bool) -> str | None:
    '''
        dmc.AccordionItem visibility is controlled by the hiddenFrom attribute.

        To hide the picker, hiddenFrom should be set to 'xs'.
        To show the picker, hiddenFrom should be set to None
    '''
    return 'xs' if hide else None
