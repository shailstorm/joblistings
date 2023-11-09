import re
from flask import request
from app import collection


def getQuery(): # returns filtersform results in the form of a query
    
    # when first loading page, all values are None. after form submission, 
    # unselected form elements have value ''. so change None to '' to standardize
    searched = request.args.get('companysearch') if request.args.get('companysearch') else ''
    departmentsearch = request.args.get('departmentsearch') if request.args.get('departmentsearch') else ''
    role     = request.args.get('role')          if request.args.get('role')          else ''
    level    = request.args.get('level')         if request.args.get('level')         else ''
    contract = request.args.get('contract')      if request.args.get('contract')      else ''

    # if checkboxes are selected, give them value True
    checkboxquery = []
    if request.args.get('new') == 'on':
        checkboxquery.append({'new':True})
    if request.args.get('featured') == 'on':
        checkboxquery.append({'featured':True})

    # create regex if user searched for a company
    if request.args.get('companysearch') is None:
        searched = ''
    else:
        searched = request.args.get('companysearch')
    companyregx = re.compile(searched, re.IGNORECASE)

    # keys in filters dict must match objects' attribute/key in database
    filters = {
               'company': companyregx, 
               'role': role, 
               'level': level, 
               'contract': contract,
               }

    # create query as list of filters, omitting filters that user did not use (those have value = '')
    query = []
    for key in filters:
        if filters[key] != '':
            query.append({key:filters[key]})

    # add new or featured filters
    query.append({ '$or' : checkboxquery }) if len(checkboxquery) > 0 else None
    
    print('******QUERY:', query) ###TEST
    return query


def getListings(): # returns all listings found under given query
    query = getQuery()
    if query:
        res = collection.find({ "$and" : query })
    else:
        res = collection.find() # if no query, returns all listings

    listings = [listing for listing in res]

    print('******LISTINGS:', f'FOUND {len(listings)} LISTINGS...', listings) ###TEST
    return listings


def getFilters(): # returns all filters selected by user

    query = getQuery() # query[0] is a dict of key:filter mappings
    filterings = []

    for item in query:
        key = list(item)[0] # key gets the only key in the dictionary
        filt = item[key] # filt gets the value of that key

        if isinstance(filt, re.Pattern): # means user searched for a company
            continue
        if key == '$or': # means user selected a checkbox
            for checkbox in filt: # structure of item['$or']: [{'new':True}, {'featured':True}]
                k = list(checkbox)[0]
                filterings.append(k) # appends 'new' or 'featured'
        else: # filt is a value to search for in database
            filterings.append(filt)

    print('******FILTERS: ', filterings) ###TEST
    return filterings