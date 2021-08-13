#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

def is_rollback_comment(comment: str) -> bool:
    """
    Reverted 1 edit by 174.255.5.246 (talk)
    Reverted edits by 73.120.245.116 (talk) to last version by Theinstantmatrix
    :param comment:
    :return:
    """
    res = False
    comment_split = comment.split(' ')

    # Reverted edits by [[Special:Contribs/Ayangkp9|Ayangkp9]] ([[User talk:Ayangkp9|talk]]) to last version by 103.251.217.221
    # Reverted edits by [[Special:Contribs/150.107.103.155|150.107.103.155]] ([[User talk:150.107.103.155|talk]]) to last version by AntiCedros
    if comment.startswith('Reverted edits by [[Special:Contrib') or \
            comment.startswith('[[Help:Reverting|Reverted]] edits by [[Special:Contrib'):
        res = True

    if (comment.startswith('Reverted edits by') and 'to last version' in comment) or \
            (comment.startswith('[[Help:Reverting|Reverted]] edits by') and 'to last version' in comment):
        res = True

    if (comment.startswith('Reverted') or comment.startswith('[[Help:Reverting|Reverted]]')) and \
            len(comment_split) > 2 and \
            (comment_split[2] == 'edit' or comment_split[2] == 'edits') and \
            comment_split[1].isdigit() and int(comment_split[1]) > 0:
        res = True

    return res


def is_undo_comment(comment: str) -> bool:
    """
    Comment example
    Undid revision 934026796 by User (talk)
    :param comment:
    :return:
    """
    res = False
    if comment.startswith('Undid revision') and \
            len(comment.split(' ')) > 2 and \
            comment.split(' ')[2].isdigit() and \
            int(comment.split(' ')[2]) > 0:
        res = True
    if comment.startswith('[[WP:UNDO|Undid]] revision') and \
            len(comment.split(' ')) > 2 \
            and comment.split(' ')[2].isdigit() and \
            int(comment.split(' ')[2]) > 0:
        res = True
    return res


def is_revert_popup_comment(comment: str) -> bool:
    """
    Comment example
    Revert to revision 934021422 dated 2020-01-04 08:50:50 by User using popups
    Revert to revision dated 13:26, 6 March 2006 by Wayward, oldid 42476405 using popups
    :param comment:
    :return:
    """

    res = False
    if comment.startswith('Revert to revision') or comment.startswith('Reverted to revision'):
        if len(comment.split(' ')) > 3:
            if comment.split(' ')[3].isdigit() and int(comment.split(' ')[3]) > 0:
                res = True
            else:
                if ' oldid ' in comment:
                    res = True
                else:
                    res = False
        else:
            res = False
    else:
        res = False

    # if (comment.startswith('Revert to revision') and comment.split(' ')[3].isdigit()) or \
    #         (comment.startswith('Reverted to revision') and comment.split(' ')[3].isdigit()):
    #     res = True
    # if (comment.startswith('Revert to revision') and not comment.split(' ')[3].isdigit() and 'oldid' in comment) or \
    #         (comment.startswith('Reverted to revision') and not comment.split(' ')[3].isdigit() and 'oldid' in comment):
    #     res = True
    return res


def count_all_cancellation(revision):
    cancellations_ids = set()
    comment = ''
    for r in revision:
        comment = r['comment'] if len(r['comment']) > 0 else r['commenthidden']
        revid = r['revid']

        if is_rollback_comment(comment):
            cancellations_ids.add(revid)
        
        if is_undo_comment(comment):
            cancellations_ids.add(revid)
        
        if is_revert_popup_comment(comment):
            cancellations_ids.add(revid)
    return cancellations_ids       
