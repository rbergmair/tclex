def normalize_geo( text ):
  
  _TO_REPLACE_HIGH_PRIORITY = {
      '/': ' / ',
      ' AN DER ': ' / ',
      ' IN DER ': ' / ',
      ' BEI DER ': ' / ',
      ' IN THE ': ' / '
    };
  
  _TO_REPLACE = {
      'Ö': 'O', 'OE': 'O', 'Ä': 'A', 'AE': 'A', 'Ü': 'U', 'UE': 'U',
      'ß': 'SS', 'SZ': 'SS', ' ST ': 'SANKT ', ' ST.': 'SANKT ',
      ' AM ': ' / ', ' AN ': ' / ', ' IM ': ' / ', ' IN ': ' / ',
      ' BEI ': ' / ', '-': ' ', '_': ' ', '.': ' ', ',': ' ', "'": ''
    };
  
  temp = text.split( ' ' );
  text = '';
  
  for e in temp:
    if e != '':
      text += ' ' + e;
      
  text = ' ' + text.upper() + ' ';
  
  for ( e, e_ ) in _TO_REPLACE_HIGH_PRIORITY.items():
    text = text.replace( e, e_ );
    
  for ( e, e_ ) in _TO_REPLACE.items():
    text = text.replace( e, e_ );
                
  cleantext = '';
  
  for e in text.split( ' ' ):
    if e != '':
      cleantext += ' ' + e;
  
  return cleantext.strip();
