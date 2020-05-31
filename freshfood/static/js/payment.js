const form = document.querySelector('#payment');
const submit = document.querySelector('#payment input[type="submit"]');

const clientToken = document.querySelector('#client-token').value;

braintree.client.create(
  {
    authorization: clientToken,
  },
  function (clientErr, clientInstance) {
    if (clientErr) {
      console.log(clientErr);
      return;
    }

    braintree.hostedFields.create(
      {
        client: clientInstance,
        styles: {
          input: { 'font-size': '13px' },
          'input.invalid': { color: 'red' },
          'input.valid': { color: 'green' },
        },
        fields: {
          number: { selector: '#card-number' },
          ccv: { selector: '#ccv' },
          expirationDate: { selector: '#expiration-date' },
        },
      },
      function (hostedFieldsErr, hostedFieldsInstance) {
        if (hostedFieldsErr) {
          console.log(hostedFieldsErr);
          return;
        }

        submit.removeAttribute('disabled');

        form.addEventListener('submit', function (e) {
          e.preventDefault();

          hostedFieldsInstance.tokenize(function (tokenizeErr, payload) {
            if (tokenizeErr) {
              console.log(tokenizeErr);
              return;
            }

            // set nonce to send to server
            document.getElementById('nonce').value = payload.nonce;
            // submit form
            form.submit();
          }, false);
        });
      }
    );
  }
);
