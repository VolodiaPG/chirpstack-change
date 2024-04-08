{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";
  outputs = inputs:
    with inputs; (
      flake-utils.lib.eachDefaultSystem
      (system: let
        pkgs = import nixpkgs {
          inherit system;
        };
        mypython = pkgs.python3.withPackages (ps:
          with ps; [
            grpcio
            chirpstack-api
            python-dotenv
          ]);
      in {
        formatter = pkgs.alejandra;
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            mypython
            pyright
            ruff
            git
            just
          ];
        };
      })
    );
}
