
# Understanding the data structure

the definitions are nested in a `<div> id='articleWRD'` and its `<table> class='WRD'`# elements, further nested like so:

```html
 <tr class='wrtopsection'>
   <td colspan='3' title='Principal Translations'>
     <strong>Principal Translations</strong>
   </td>
 </tr>
 <tr class='langHeader' style='font-size: 13px;text-decoration: underline;font-weight:bold;'>
   <td class='FrWrd'>Spanish</td>
   <td></td>
   <td class='ToWrd'>English</td>
 </tr>
 <tr class='even' id='esen:18465'>
   <td class='FrWrd' >
     <strong>vamos</strong> <em class='tooltip POS2'>expr<span><i>expresión</i>: Expresiones idiomáticas, dichos, refranes y frases hechas de tres o más palabras ("Dios nos libre", "a lo hecho, pecho").</span></em>
   </td>
   <td> (para instar, urgir)</td>
   <td class='ToWrd' >
     let´s go, come on <em class='tooltip POS2'>interj<span><i>interjection</i>: Exclamation--for example, "Oh no!"  "Wow!"</span></em>
   </td>
 </tr>
 <tr class='even'>
   <td>&nbsp;</td>
   <td colspan='2' class='FrEx'>Vamos, hay que darse prisa que se nos hace tarde.</td>
 </tr>
```

## Important sections

```html
 <tr class='wrtopsection'>
   <td title='Principal Translations'>
     <strong>________</strong>
   </td>
 </tr>
 <tr class='langHeader'>
   <td class='FrWrd'>Spanish</td>
   <td></td>
   <td class='ToWrd'>English</td>
 </tr>
 <tr id='esen:18465'>
   <td class='FrWrd' >
     <strong>vamos</strong>
     <em class='tooltip POS2'>expr
       <span>
         <i>expresión</i>:
           Expresiones idiomáticas, dichos, refranes y frases hechas
           de tres o más palabras ("Dios nos libre", "a lo hecho, pecho").
       </span>
     </em>
   </td>
   <td> (para instar, urgir)</td>
   <td class='ToWrd' >
     let´s go, come on
     <em class='tooltip POS2'>interj
       <span>
         <i>interjection</i>: Exclamation--for example, "Oh no!"  "Wow!"
       </span>
     </em>
   </td>
 </tr>
 <tr>
   <td></td>
   <td class='FrEx'>Vamos, hay que darse prisa que se nos hace tarde.</td>
 </tr>
```
