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
          input: { 'font-size': '1.2rem', border: '1px solid red' },
          'input.invalid': { color: 'red' },
          'input.valid': { color: 'green' },
        },
        fields: {
          number: {
            selector: '#card-number',
            placeholder: '4111 1111 1111 1111',
          },
          cvv: { selector: '#cvv', placeholder: '123' },
          expirationDate: {
            selector: '#expiration-date',
            placeholder: '10/2022',
          },
        },
      },
      function (hostedFieldsErr, hostedFieldsInstance) {
        if (hostedFieldsErr) {
          console.log(hostedFieldsErr);
          return;
        }

        submit.removeAttribute('disabled');

        form.addEventListener(
          'submit',
          function (e) {
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
            });
          },
          false
        );
      }
    );
  }
);
